"""C-40: for every acceptance predicate, the mutation that MUST redden it.

Each mutation is a literal source edit applied to a working copy of
`taskboard/views.py`, run against the named test, then reverted. A mutation that
leaves the test green means the predicate does not certify what it claims.

Run:  python .fast-dev-flow/probes/_mutate.py
"""
import subprocess, sys, pathlib

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
VIEWS = ROOT / "taskboard" / "views.py"

# (label, test node, [(find, replace), ...])
MUTATIONS = [
    ("AC-1 gutter (task): GUTTER = 0",
     "tests/test_gantt.py::test_a_truncated_title_never_touches_its_own_bar",
     [("\nGUTTER = 2", "\nGUTTER = 0")]),

    ("AC-2 gutter (project): drop the name's clip allowance",
     "tests/test_gantt.py::test_a_truncated_project_name_never_touches_the_field",
     [("clip(p.name,\n                                                     geo.label_w - 2 - GUTTER)",
       "clip(p.name,\n                                                     geo.label_w - 2)")]),

    ("AC-3 guide: FIELD_WEEK = LATTICE (guide becomes the ground)",
     "tests/test_gantt.py::test_the_field_is_ruled_by_weeks",
     [('FIELD_WEEK = "┆"', 'FIELD_WEEK = "·"')]),

    ("AC-3 guard: the guide may take the today column",
     "tests/test_gantt.py::test_the_field_is_ruled_by_weeks",
     [("if d.weekday() == 0 and cell != today_cell:",
       "if d.weekday() == 0:")]),

    ("AC-4 months: the axis stops being told about them",
     "tests/test_gantt.py::test_the_axis_names_the_months",
     [("_scale_with_note(geo, inner, note, months) if note\n                           else _scale_row(geo, inner, months)",
       "_scale_with_note(geo, inner, note) if note\n                           else _scale_row(geo, inner)")]),

    ("AC-4 months: a month name may be half-printed",
     "tests/test_gantt.py::test_the_axis_names_the_months",
     [("        if any(body[at + i] != \" \" for i in range(-1, len(name) + 1)\n"
       "               if 0 <= at + i < span):\n            continue\n",
       "")]),

    ("AC-5 reach: the slab comes back",
     "tests/test_gantt.py::test_the_project_reach_is_a_rule_not_a_slab",
     [('FIELD_REACH = "━"', 'FIELD_REACH = "█"')]),

    # The first attempt here was GUTTER=3 with the project clip left at
    # `label_w - 2`. It SURVIVED, and correctly so: `fit` still pads the label to
    # exactly `label_w - 2`, so that mutation removes the project's gutter
    # without ever changing a row's width. It was a bad mutation, not a weak
    # test. The width law's real hinge is the pairing between the title's width
    # and the band's slice — break that and every task row grows a cell.
    ("AC-6 width: the title takes a cell the band does not give back",
     "tests/test_cells.py",
     [("tw = geo.label_w - 3 + over", "tw = geo.label_w - 2 + over")]),

    ("legend ghost: an entry for a mark the view never draws",
     "tests/test_legend.py",
     [('        if gweeks:\n            out.append((c(LATTICE + FIELD_WEEK + LATTICE, "dim"),\n'
       '                        "the week guide: every dashed rule is a monday"))',
       '        if True:\n            out.append((c("\\u2591\\u2591\\u2591", "dim"),\n'
       '                        "a mark this view does not draw"))')]),
]

original = VIEWS.read_text(encoding="utf-8")
rows = []
try:
    for label, node, edits in MUTATIONS:
        src = original
        ok = True
        for find, repl in edits:
            if find not in src:
                rows.append((label, node, "PATCH DID NOT APPLY"))
                ok = False
                break
            src = src.replace(find, repl, 1)
        if not ok:
            continue
        VIEWS.write_text(src, encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", node, "-q", "--no-header",
                            "-x", "-p", "no:cacheprovider"],
                           cwd=ROOT, capture_output=True, text=True)
        rows.append((label, node, "REDDENS ✓" if r.returncode else "SURVIVED ✗ (INERT)"))
finally:
    VIEWS.write_text(original, encoding="utf-8")

print(f"{'mutation':58s} {'verdict'}")
print("-" * 86)
for label, node, verdict in rows:
    print(f"{label:58s} {verdict}")
    print(f"{'':58s} {node.split('::')[-1]}")
bad = [r for r in rows if "REDDENS" not in r[2]]
print("\n" + ("ALL MUTATIONS REDDEN THEIR PREDICATE"
              if not bad else f"{len(bad)} PROBLEM(S) — see above"))
print("views.py restored:", VIEWS.read_text(encoding="utf-8") == original)
