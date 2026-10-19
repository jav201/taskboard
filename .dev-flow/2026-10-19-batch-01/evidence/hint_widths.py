"""PC-4 (batch 2026-10-19-batch-01): the hint row's first widths, measured with
`rich.cells.cell_len` over the LITERAL wording strings of LLR-2104.1 and the
shipped views-1/2 wordings — outside the code under test. The tables the tests
hold are pasted from this output.

    python .dev-flow/2026-10-19-batch-01/evidence/hint_widths.py
"""
from rich.cells import cell_len

NAMES = {"  ": "1 gantt  2 split  3 all  ", " ": "1 gantt 2 split 3 all "}
V12 = {
    "gantt": [("long", "  ", "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"),
              ("middle", "  ", "⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),
              ("short", " ", "⇥ · ←→ · ␣ hide · a all · x export · esc"),
              ("compact", " ", "⇥ ←→ ␣ x esc"),
              ("esc", " ", "esc")],
    "split": [("long", "  ", "pgdn notes · ⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"),
              ("middle", "  ", "pgdn · ⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc"),
              ("short", " ", "pgdn · ⇥ · ←→ · ␣ hide · a all · x export · esc"),
              ("compact", " ", "pgdn ⇥ ←→ ␣ x esc"),
              ("esc", " ", "esc")],
    "all-rail": [("long", "  ", "⇥ next · ↑↓ move · ←→ rail/timeline · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave"),
                 ("middle", "  ", "⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc"),
                 ("compact", " ", "⇥ ↑↓ ←→ ␣ ⇧↑↓ enter a x esc"),
                 ("esc", " ", "esc")],
    "all": [("long", "  ", "⇥ next · ←→ ↑↓ move · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave"),
            ("middle", "  ", "⇥ · ←→ ↑↓ · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc"),
            ("compact", " ", "⇥ ←→ ↑↓ ␣ ⇧↑↓ enter a x esc"),
            ("esc", " ", "esc")],
}


def first_widths(view: str, hidden: int) -> dict[str, int]:
    """The first width (36..200) at which each wording is the one painted."""
    tail = f" · u {hidden} hidden" if hidden else ""
    out: dict[str, int] = {}
    lo, hi = (100, 200) if view == "all-rail" else ((36, 99) if view == "all" else (36, 200))
    for w in range(lo, hi + 1):
        for tier, gap, keys in V12[view]:
            if cell_len(NAMES[gap] + keys + tail) <= w - 2:
                break
        out.setdefault(tier, w)
    return out


if __name__ == "__main__":
    for view in V12:
        for hidden in (0, 1, 3, 10):
            print(f"({view!r}, {hidden}): {first_widths(view, hidden)},")
