"""Mutant spec for increment 004 (the one-time milestone offer). Run from the repo root:
    python mk_mutants_inc004.py <export dir>"""
import json
import sys

exp = sys.argv[1]
M, A, D = "taskboard/models.py", "taskboard/app.py", "taskboard/modals.py"
T = ["tests/test_milestone_offer.py", "tests/test_milestone_offer_seam.py"]
m = [
    ("O1", M, '        if t.start_date is None or t.start_date == "":\n',
     '        if parse_iso(t.start_date) != due:\n', "a start ≠ due task grouped as due-only"),
    ("O2", M, "    rows.sort(key=lambda r: (not r[0], r[1], r[2]))\n", "    rows.sort(key=lambda r: r[2])\n",
     "candidates in board order"),
    ("O3", M, '    return (isinstance(m, dict) and type(m.get("milestones")) is int\n            and m.get("milestones") == MILESTONES_MIGRATION)',
     '    return isinstance(m, dict) and bool(m.get("milestones"))', "the mark read with bool()"),
    ("O4", M, "            raw = target.read_bytes()\n            result.backup = _create_beside(target, MILESTONE_BACKUP, raw).name\n",
     "            raw = b\"\"\n            result.backup = _create_beside(target, MILESTONE_BACKUP, raw).name\n",
     "the backup not the file's bytes"),
    ("O5", M, '        mark["milestones"] = MILESTONES_MIGRATION\n', "        pass\n", "no mark recorded"),
    ("O6", M, "            try:\n                (target.parent / name).unlink(missing_ok=True)\n            except OSError:\n                pass\n",
     "            (target.parent / name).unlink(missing_ok=True)\n", "cleanup not best-effort (S-4)"),
    ("O7", M, "        for t, m0, s0 in before:                 # the board first …\n            t.milestone, t.start_date = m0, s0\n",
     "        for t, m0, s0 in before:                 # the board first …\n            pass\n", "a failure leaves the flags on"),
    ("O8", M, "    convert = [t for t in cands if t.id in picked]          # each at most once\n",
     "    convert = [t for t in board.tasks if t.id in picked]\n", "a chosen non-candidate converted"),
    ("O9", M, '                        settings={"migrations": {"links": LINKS_MIGRATION,\n                                                 "milestones": MILESTONES_MIGRATION}})',
     '                        settings={"migrations": {"links": LINKS_MIGRATION}})', "a seeded board unmarked"),
    ("O10", A, "            run_milestone_offer(self.board, [])\n            return\n", "            return\n",
     "a no-candidate board left unmarked"),
    ("O11", A, '            if "milestones" in entry:\n', "            if False:\n", "no one-step undo of the conversion"),
    ("O12", A, '        late = (f" · {result.ineligible} no longer eligible" if result.ineligible else "")\n',
     '        late = ""\n', "the toast hides the ineligible count"),
    ("O13", D, '        self.query_one("#offer-keys", Label).update(self._offer_keys())\n', "",
     "the keys row's N goes stale"),
    ("O14", D, "        self.dismiss([self._rows[i].id for i in range(len(self._rows)) if self._on[i]])\n",
     "        self.dismiss([self._rows[i].id for i in range(len(self._rows))])\n", "↵ returns every row"),
    ("O15", D, "    def action_not_now(self) -> None:\n        self.dismiss([])\n",
     "    def action_not_now(self) -> None:\n        self.dismiss([t.id for t in self._rows])\n", "esc converts every row"),
    ("O16", D, "        self.query_one(\"#offer-list\", OptionList).styles.max_height = max(3, height - 6)\n",
     "        pass\n", "the list unbounded (the keys row pushed off)"),
    ("O17", M, '        if had_mark:\n            board.settings["migrations"] = old_mark\n        else:\n            board.settings.pop("migrations", None)\n        for name in made:',
     "        for name in made:", "a failure keeps the mark"),
    ("O18", A, "        # LAST: the one-time milestone offer covers whatever start opened (the\n        # identity picker included) until it is answered (D-615)\n        self._offer_milestones()\n",
     "", "no offer at start"),
]
spec = {"export": exp, "mutants": [dict(id=i, file=f, old=o, new=n, what=w, tests=T)
                                   for i, f, o, n, w in m]}
json.dump(spec, open(exp + "/spec.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
spec["export"] = "<scratch>/bat004"
json.dump(spec, open(".dev-flow/2026-10-04-batch-02/evidence/mutants_inc004.json", "w",
                     encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(m))
