"""Insert the cost-model prose into views.py WITHOUT touching its CRLF endings.

Prose only. Verified afterwards by an AST comparison: the module's code must be
identical before and after -- a docstring change that alters behaviour is not a
docstring change.
"""
import ast, hashlib
from pathlib import Path

VIEWS = Path(__file__).resolve().parents[2] / "taskboard" / "views.py"

ALLOCATE_ANCHOR = "    lead would stop being the hero.\"\"\""
ALLOCATE_NEW = '''    lead would stop being the hero.

    THE CHARGE, AND IT IS ONLY HALF THE MODEL. This bills
    `prof + sum(wrows + min(titles, o)) + n_rest`, but `lead_band` DRAWS
    `prof + 2` -- a head and a tail that `prof` does not count. The missing two
    rows are paid at the call site (`swimlane_plan`), which is where the whole
    identity is written down. Read either half on its own and the model is off
    by two in whichever direction you read it; that mistake, in both directions,
    is what `.dev-flow/05-postmortem.md` is about. `tests/test_row_cost.py`
    pins the two halves together, so neither can move alone."""'''

PLAN_ANCHOR = "    twice with different numbers is how a cursor ends up on an undrawn task.\"\"\""
PLAN_NEW = '''    twice with different numbers is how a cursor ends up on an undrawn task.

    THE ROW COST MODEL, in one place, because it was derived three times and
    disagreed with itself each time:

        PANEL (h rows)                 BODY
          1  header                      lead    = prof + 2   [only when active]
          B  body                        stack_i = wrows + min(titles, nameable_i)
          A  absence line, A in {0,1}    rest    = n_rest
          1  axis
          0  close -- `bottom()` returns "", the view being frameless

        room = h - 2 - 2*[active]      need = prof + sum(...) + n_rest
        BODY == need + 2*[active]      2 + BODY + A == h

    THE TWO `2`s ARE NOT THE SAME `2`. The `h - 2` is the panel's OWN CHROME --
    the header and the axis. The `- 2*[active]` is THE LEAD BAND'S head and
    tail, the two rows `allocate` never bills for. Collapse them in either
    direction and the panel overflows (shedding work it should have drawn) or
    pads (on a view whose whole design is that it does not).

    REGIME -- the identity holds when a lane is active AND an allocation fits.
    Outside it two things happen, both documented and neither a defect: with NO
    active lane, `prof` is billed for a bench nothing draws and the view PADS;
    with no feasible allocation, the renderer sheds blocks and says `+N not
    shown`. `tests/test_row_cost.py` pins all three cases."""'''


def main():
    raw = VIEWS.read_bytes()
    before = raw.decode("utf-8")
    eol = "\r\n" if b"\r\n" in raw else "\n"
    tree_before = ast.dump(ast.parse(before))

    out = before
    for anchor, new in ((ALLOCATE_ANCHOR, ALLOCATE_NEW), (PLAN_ANCHOR, PLAN_NEW)):
        a = anchor.replace("\n", eol)
        n = out.count(a)
        assert n == 1, f"anchor matched {n} times, expected 1: {anchor[:50]!r}"
        out = out.replace(a, new.replace("\n", eol))

    VIEWS.write_bytes(out.encode("utf-8"))
    after = VIEWS.read_bytes().decode("utf-8")

    # 1. line endings unchanged
    assert b"\r\n" in VIEWS.read_bytes() if eol == "\r\n" else True
    bare = VIEWS.read_bytes().count(b"\n") - VIEWS.read_bytes().count(b"\r\n")
    print(f"eol={eol!r}  bare-LF introduced: {bare}")

    # 2. THE REAL CHECK: strip every docstring and compare the code
    def strip_docs(src):
        t = ast.parse(src)
        for node in ast.walk(t):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef, ast.Module)):
                body = node.body
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    node.body = body[1:] or [ast.Pass()]
        return ast.dump(ast.fix_missing_locations(t))

    same_code = strip_docs(before) == strip_docs(after)
    changed_at_all = tree_before != ast.dump(ast.parse(after))
    print(f"code identical after stripping docstrings: {same_code}")
    print(f"docstrings actually changed:               {changed_at_all}")
    assert same_code, "BEHAVIOUR CHANGED -- this was supposed to be prose only"
    assert changed_at_all, "nothing changed"
    print(f"sha256 {hashlib.sha256(VIEWS.read_bytes()).hexdigest()[:16]}")


main()
