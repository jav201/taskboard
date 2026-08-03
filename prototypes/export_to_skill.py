"""export_to_skill.py -- regenerate the tui-design skill's language assets from
the running implementation.

    python prototypes/export_to_skill.py [SKILL_DIR]

WHY THIS EXISTS.  The skill's `assets/languages.py` drifted badly from the code
that actually renders these languages, and the drift was invisible until someone
went looking: the app rendered ten languages, the skill listed eight; Solari and
Blueprint had never reached the skill at all; Ledger existed there only as an
imported picture, not as a language; and phosphor and bbs, retired from the
prototype on 2026-07-26 by operator curation, were still being offered as
implemented.  Worse, the skill's token dicts held colour and a few structural
keys that NO renderer read -- which is precisely the failure `LANGUAGES.md`
itself names ("A language definition is code, not a manifest").  The skill was
preaching what its own asset broke.

A hand-written copy drifts again the moment either side moves.  So the asset is
a PROJECTION of the implementation, produced here, and the file it writes says
so in its own header along with the command that rebuilds it.

WHAT IT WRITES.  One file, `<skill>/assets/languages.py`, containing:

  LANGUAGES  every token of every language, exactly as `themes.py` holds them
  FAMILY     each language's board layout family, from `Kit.board_layout()`
  DOC        each Kit's class docstring -- the doctrine, from the code
  ORDER      the ten, in the order the app cycles them
  RETIRED    the two the operator removed, with the reason, so the skill can
             still OFFER them as design options while being honest that the
             reference implementation no longer renders them

WHAT IT DELIBERATELY DOES NOT DO.  It does not touch `LANGUAGES.md`.  The
catalogue is prose that argues; a generator would flatten it into a data dump
and lose the part that teaches.  The doctrine is carried into the asset via
DOC so a reader has both, and the prose is edited by hand.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import taskboard.language as LG                                   # noqa: E402
import taskboard.themes as TH                                     # noqa: E402

DEFAULT_SKILL = Path.home() / ".claude" / "skills" / "tui-design"

# The two the operator retired from the prototype on 2026-07-26.  They are not
# deleted here: a retired IMPLEMENTATION is not an invalid design language, and
# the skill's job is to offer options.  What would be dishonest is listing them
# as though a kit still rendered them.
RETIRED = {
    "phosphor": ("one hue at many lightnesses (amber/green CRT); severity must "
                 "ride brightness and glyph, never a second hue",
                 "retired from the reference app 2026-07-26 by operator "
                 "curation -- still a valid language to choose"),
    "bbs": ("full 16 colours, solid ink, double-line box drawing, "
            "block-gradient shading (ANSI/BBS art)",
            "retired from the reference app 2026-07-26 by operator "
            "curation -- still a valid language to choose"),
}

HEADER = '''r"""languages.py -- the ten visual languages, AS IMPLEMENTED.

DO NOT EDIT BY HAND.  This file is generated from the reference implementation
by `prototypes/export_to_skill.py` in the taskboard repo:

    cd {root}
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\\export_to_skill.py

WHY IT IS GENERATED.  The previous hand-written version drifted from the code
without anyone noticing: it listed eight languages where the app rendered ten,
it had never heard of Solari or Blueprint, it kept offering phosphor and bbs as
implemented after they were retired, and its structural tokens were read by no
renderer at all -- the exact "a language definition is code, not a manifest"
failure LANGUAGES.md warns about, committed by the file the doc points at.

WHAT EACH NAME MEANS

    LANGUAGES  every token, as `themes.py` holds it.  Structural tokens
               (`layout`, `hero`, `frame`, `meter`, `base`, `sel`, `tempo`...)
               are READ BY RENDERERS in the reference app -- mutate one and the
               render changes, which is the property that keeps a token from
               being dead metadata.  `prototypes/verify_language.py` asserts it.
    FAMILY     the board layout family: columns | sections | split.
    DOC        each language's doctrine, taken from its Kit class docstring, so
               the prose here cannot drift from the class it describes.
    ORDER      the ten in the order the app's `t` key cycles them.
    RETIRED    two languages the operator removed from the reference app.  They
               remain legitimate choices -- see LANGUAGES.md -- but no kit here
               renders them, and pretending otherwise is what this entry exists
               to prevent.

USING IT

    from languages import LANGUAGES, DOC, FAMILY, ORDER
    tok = LANGUAGES["solari"]        # every token, including the structural ones
    print(DOC["solari"])             # why it commits to what it commits to

Reference frames for all ten live in `assets/languages/` -- board and component
sheet each, one sweep, one fixture, one viewport.  A page that puts the frames,
the tokens and the doctrine side by side is generated by
`prototypes/build_languages_html.py`.

Generated {when} from {n} kits in `taskboard/language.py`.
"""
from __future__ import annotations

'''


def fmt(v) -> str:
    return repr(v)


def build(root: Path, when: str) -> str:
    langs = TH.ORDER
    out = [HEADER.format(root=root, when=when, n=len(langs))]

    out.append("LANGUAGES: dict[str, dict] = {\n")
    for n in langs:
        t = {k: v for k, v in TH.THEMES[n].items()
             if isinstance(v, (str, int, float, bool))}
        label = t.get("label", n.title())
        note = t.get("note", "")
        out.append(f"    # {label} -- {note}\n" if note else f"    # {label}\n")
        out.append(f"    {n!r}: dict(\n")
        # structural first, then palette, then the rest -- reading order
        struct = ["layout", "hero", "frame", "meter", "base", "numbered",
                  "sel", "tempo", "easing"]
        pal = ["ground", "ink", "mut", "dim", "accent", "warn", "alert",
               "panel", "focus", "screen", "alu"]
        seen = set()
        for group in (struct, pal):
            line = "        "
            for k in group:
                if k in t:
                    seen.add(k)
                    piece = f"{k}={fmt(t[k])}, "
                    if len(line) + len(piece) > 78:
                        out.append(line.rstrip() + "\n")
                        line = "        "
                    line += piece
            if line.strip():
                out.append(line.rstrip() + "\n")
        rest = [k for k in sorted(t) if k not in seen]
        line = "        "
        for k in rest:
            piece = f"{k}={fmt(t[k])}, "
            if len(line) + len(piece) > 78:
                out.append(line.rstrip() + "\n")
                line = "        "
            line += piece
        if line.strip():
            out.append(line.rstrip() + "\n")
        out.append("    ),\n")
    out.append("}\n\n")

    out.append("# board layout family, from Kit.board_layout()\n")
    out.append("FAMILY: dict[str, str] = {\n")
    for n in langs:
        out.append(f"    {n!r}: {LG.kit(n).board_layout()!r},\n")
    out.append("}\n\n")

    out.append("# The doctrine, straight off each Kit class -- edit it THERE.\n")
    out.append("DOC: dict[str, str] = {\n")
    for n in langs:
        doc = inspect.getdoc(type(LG.kit(n))) or ""
        out.append(f"    {n!r}: '''{doc}''',\n")
    out.append("}\n\n")

    out.append(f"ORDER: list[str] = {langs!r}\n\n")

    out.append("# Retired from the reference app -- still valid to CHOOSE.\n")
    out.append("RETIRED: dict[str, tuple[str, str]] = {\n")
    for k, (commits, why) in RETIRED.items():
        out.append(f"    {k!r}: (\n        {commits!r},\n        {why!r}),\n")
    out.append("}\n")
    return "".join(out)


def main() -> int:
    skill = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SKILL
    dst = skill / "assets" / "languages.py"
    if not dst.parent.exists():
        print(f"NO SUCH SKILL ASSETS DIR: {dst.parent}", file=sys.stderr)
        return 2
    # the date is passed in rather than read from the clock so a rebuild that
    # changes nothing produces no diff
    when = "2026-08-02"
    src = build(ROOT, when)
    dst.write_text(src, encoding="utf-8")
    print(f"  wrote {dst} ({len(src) / 1024:.0f} KB, {len(TH.ORDER)} languages)")

    # prove the generated file actually imports and holds what it claims
    ns: dict = {}
    exec(compile(src, str(dst), "exec"), ns)
    assert ns["ORDER"] == TH.ORDER, "ORDER drifted"
    assert set(ns["LANGUAGES"]) == set(TH.ORDER), "LANGUAGES drifted"
    for n in TH.ORDER:
        got = ns["LANGUAGES"][n]
        want = {k: v for k, v in TH.THEMES[n].items()
                if isinstance(v, (str, int, float, bool))}
        assert got == want, f"{n}: tokens differ"
        assert ns["DOC"][n] == (inspect.getdoc(type(LG.kit(n))) or ""), f"{n}: doc"
        assert ns["FAMILY"][n] == LG.kit(n).board_layout(), f"{n}: family"
    print(f"  verified: {len(TH.ORDER)} languages, every token, doc and family "
          f"round-trips")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
