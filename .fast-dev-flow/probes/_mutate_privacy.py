"""Every law in test_privacy_sweep.py must redden under a mutation that breaks
exactly what it claims to protect -- and the OTHER laws must stay green, so the
harness proves each test is load-bearing rather than that the file as a whole
is sensitive to damage.
"""
import re, subprocess, sys, os

os.chdir(r"C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants")
SRC = "tools/privacy_sweep.py"
ORIG = open(SRC, encoding="utf-8").read()

MUTS = [
    ("prefixes() collapses to the whole string only",
     lambda t: t.replace("    return [s[:k] for k in range(len(s), MIN_PREFIX - 1, -1)]",
                         "    return [s]"),
     "test_a_name_that_reached_the_file_truncated_is_still_found"),
    ("MIN_PREFIX floor dropped to 3 (over-reports ordinary words)",
     lambda t: t.replace("MIN_PREFIX = 10", "MIN_PREFIX = 3"),
     "test_an_ordinary_word_from_a_real_name_is_not_a_leak"),
    ("MIN_STRING dropped to 1 (protects bare words)",
     lambda t: t.replace("MIN_STRING = 12", "MIN_STRING = 1"),
     "test_a_short_record_is_not_protected_and_the_floor_is_stated"),
    ("sweep never matches",
     lambda t: t.replace("            if needle in text:", "            if False:"),
     "test_a_planted_whole_name_is_found"),
    ("sweep matches every file unconditionally",
     lambda t: t.replace("            if needle in text:", "            if True:"),
     "test_a_clean_tree_reports_nothing"),
    (".svg added to the skip list (rich writes captures as svg)",
     lambda t: t.replace('SKIP_SUFFIXES = {".png"', 'SKIP_SUFFIXES = {".svg", ".png"'),
     "test_binary_suffixes_are_skipped_not_silently_decoded"),
    ("board_strings stops sorting longest-first",
     lambda t: t.replace("                  key=len, reverse=True)", "                  key=len)"),
     "test_the_longest_match_is_reported_not_a_prefix_of_it"),
]


def run(*args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q",
                        "tests/test_privacy_sweep.py", *args],
                       capture_output=True, text=True)
    return r.stdout + r.stderr


rows = []
for name, mutate, target in MUTS:
    new = mutate(ORIG)
    if new == ORIG:
        rows.append("NOT APPLIED  %s" % name)
        continue
    open(SRC, "w", encoding="utf-8", newline="").write(new)
    try:
        targeted = run("-k", target)
        whole = run()
    finally:
        open(SRC, "w", encoding="utf-8", newline="").write(ORIG)
    killed = "failed" in targeted or "error" in targeted.lower()
    n_fail = len(re.findall(r"FAILED|failed", whole))
    rows.append("%-4s %-58s target=%s  total_failed=%d"
                % ("KILL" if killed else "SURVIVED", name, target[:40], n_fail))

baseline = run()
rows.append("")
rows.append("baseline (unmutated): %s" % [l for l in baseline.splitlines() if "passed" in l or "failed" in l][-1].strip())
print("\n".join(rows))
