"""Increment 001 mutation battery (batch 2026-10-29-batch-02): `taskboard --report`.

Each mutant is ONE fault in `taskboard/__main__.py`, applied as exact string replacements
(each `old` must occur exactly once), run against the named tests, then the file is restored
byte-identically (sha256 printed before and after). A mutant is KILLED when pytest exits
non-zero AND one of the named tests is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-02/evidence/mutation-001.py [M01 M02 ...]
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAIN = ROOT / "taskboard" / "__main__.py"
T = "tests/test_report_cli.py"

PROMPT_Q = ('''        if answer == "q":\n            print("taskboard: no board chosen", file=err)\n'''
            '''            raise SystemExit(1)''')

# (id, replacements, (-k expression, names that must go RED), what it breaks)
MUTANTS = [
    ("M01", [("    registry = _read_registry()\n    wanted",
              "    registry = Registry.load(registry_path(), default_board_path())\n    wanted")],
     ("TC_4110", ["test_TC_4110_a_corrupt_registry_people_and_marks_are_not_copied_aside"]),
     "LLR-4104.2: the registry read with `load`, which copies an unreadable file aside"),
    ("M02", [("""            print(f"Not a choice: {_safe(answer)[:40]}", file=err)\n            continue\n""",
              """            pick = default\n""")],
     ("AT_4103 or TC_4103", ["test_AT_4103_q_and_an_end_of_input_after_a_bad_answer_exit_1",
                             "test_TC_4103_the_prompt_answers"]),
     "LLR-4102.2: an invalid answer takes the default instead of asking again"),
    ("M03", [("""pass --board PATH to choose a board", file=err)\n                raise SystemExit(2)""",
              """pass --board PATH to choose a board", file=err)\n                raise SystemExit(1)""")],
     ("AT_4103 or TC_4103", ["test_AT_4103_empty_piped_stdin_exits_2_with_the_list",
                             "test_TC_4103_the_prompt_answers"]),
     "LLR-4102.3: an empty piped stdin exits 1, not 2"),
    ("M04", [("            found = [e for e in active if _a_board_file(e.path)]",
              "            found = [default]")],
     ("AT_4102", ["test_AT_4102_a_writes_reports_covering_all_boards"]),
     "LLR-4102.4 negative control: `a` reads only the default board"),
    ("M05", [("    data = report_html.extract(boards, people, marks, today, project=key)",
              "    data = report_html.extract(boards, people, marks, today, project=None)")],
     ("AT_4104", ["test_AT_4104_board_flag_does_not_prompt_and_project_scopes"]),
     "LLR-4103.1 negative control: PROJECT ignored"),
    ("M06", [("""Path(primary).parent / "reports", today)""", """Path("reports"), today)""")],
     ("AT_4101", ["test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two"]),
     "LLR-4101.2 negative control: the files written beside the CWD"),
    ("M07", [("""out.append(f"  {n}. {_safe(e.name)}{'  (default)'""",
              """out.append(f"  {n}. {e.name}{'  (default)'""")],
     ("TC_4106", ["test_TC_4106_names_and_paths_are_printed_without_control_bytes"]),
     "LLR-4104.3 negative control: the raw board name printed"),
    ("M08", [("    if args.report is not None and args.board is not None and not _a_board_file(args.board):",
              "    if False:")],
     ("AT_4105", ["test_AT_4105_missing_board_path_is_refused_and_creates_nothing"]),
     "LLR-4104.1 negative control: a missing --board path is not refused (the loader seeds it)"),
    ("M09", [("        path = expand_home(source)\n        e = registry.entry_for(path)",
              "        path = expand_home(source)\n        registry.register(path)\n        e = registry.entry_for(path)")],
     ("TC_4113", ["test_TC_4113_a_board_flag_registers_nothing"]),
     "LLR-4104.2 negative control: a --board path is registered"),
    ("M10", [("""REPORT_KINDS[args.report_kind or "both"]""", """REPORT_KINDS["both"]""")],
     ("TC_4101", ["test_TC_4101_report_kind_selects_the_files"]),
     "LLR-4101.1: --report-kind ignored"),
    ("M12", [("    except OSError as exc:\n        parser.exit(1, f\"taskboard: report not written",
              "    except ZeroDivisionError as exc:\n        parser.exit(1, f\"taskboard: report not written")],
     ("TC_4111", ["test_TC_4111_a_reports_path_that_cannot_be_a_folder_exits_1"]),
     "LLR-4101.2: the write unguarded (an OSError reaches the user as a traceback)"),
    ("M13", [("        if stream is None:\n            return \"\"\n", "")],
     ("TC_4110", ["test_TC_4110_stdin_that_misbehaves_never_tracebacks"]),
     "LLR-4102.5: a closed stdin (None) raises"),
    ("M14", [("        line = os.path.abspath(p)\n", "        line = ' '.join(os.path.abspath(p).split())\n")],
     ("TC_4106", ["test_TC_4106_a_path_with_two_spaces_is_printed_unchanged"]),
     "LLR-4104.3: stdout paths collapsed"),
    ("M15", [("if e.id == default.id else", "if e.id != default.id else")],
     ("TC_4103", ["test_TC_4103_the_prompt_answers"]),
     "LLR-4102.2: the wrong board marked as the default"),
    ("M16", [(PROMPT_Q, PROMPT_Q.replace("SystemExit(1)", "SystemExit(0)"))],
     ("AT_4103", ["test_AT_4103_q_and_an_end_of_input_after_a_bad_answer_exit_1"]),
     "LLR-4102.2: `q` exits 0"),
    ("M17", [("(default if default.id in {f.id for f in found} else found[0]).path",
              "(default if default.id in {f.id for f in found} else found[-1]).path")],
     ("TC_4112", ["test_TC_4112_a_falls_back_when_the_default_board_is_unreadable"]),
     "LLR-4102.4: the fallback folder is the last readable board, not the first"),
    ("M18", [("    if skipped:\n", "    if False:\n")],
     ("TC_4104", ["test_TC_4104_a_skips_and_counts_a_missing_board"]),
     "LLR-4102.4: the skipped boards are not counted"),
    ("M20", [("    return text.translate(_DROPPED)", "    return text")],
     ("TC_4106", ["test_TC_4106_names_and_paths_are_printed_without_control_bytes"]),
     "LLR-4104.3: bidi overrides and separators kept"),
    ("M21", [("    if args.report_kind is not None and args.report is None:", "    if False:")],
     ("TC_4102", ["test_TC_4102_report_kind_is_validated"]),
     "LLR-4101.1: --report-kind accepted without --report"),
    ("M22", [("            if wanted is not None:\n                parser.exit(2, \"taskboard: --report PROJECT",
              "            if False:\n                parser.exit(2, \"taskboard: --report PROJECT")],
     ("TC_4105", ["test_TC_4105_project_with_a_is_refused"]),
     "LLR-4103.1: PROJECT with `a` accepted"),
    ("M23", [("    except OSError:\n        reg = None\n", "    except ZeroDivisionError:\n        reg = None\n")],
     ("TC_4108", ["test_TC_4108_one_board_does_not_prompt_and_a_missing_default_is_refused"]),
     "SEC-N2: a missing registry file raises instead of reading as absent"),
    ("M25", [("        if len(line.rstrip(\"\\r\\n\")) > ANSWER_MAX:", "        if False:")],
     ("TC_4110", ["test_TC_4110_stdin_that_misbehaves_never_tracebacks"]),
     "LLR-4102.5: no cap on the answer line"),
    ("M26", [("answer.isascii() and answer.isdecimal() and ", "answer.isdecimal() and ")],
     ("TC_4103", ["test_TC_4103_the_prompt_answers"]),
     "LLR-4102.2: a non-ASCII digit read as a pick"),
    ("M27", [("        return stream is not None and stream.isatty()", "        return stream is not None")],
     ("TC_4103", ["test_TC_4103_the_prompt_answers"]),
     "LLR-4102.3: every stream counts as a terminal (the exit-2 rule never fires)"),
    ("M28", [("        if not _a_board_file(pick.path):\n            print(f", "        if False:\n            print(f")],
     ("TC_4103", ["test_TC_4103_a_picked_board_whose_file_is_gone_asks_again"]),
     "LLR-4102.2: a picked board whose file is gone is accepted"),
    ("M29", [("        except UnicodeEncodeError:          # a console codepage that cannot spell the path", "        except ZeroDivisionError:")],
     ("TC_4114", ["test_TC_4114_a_stdout_that_cannot_spell_the_path_still_prints_it"]),
     "stdout encoding: an unspellable path raises after the files are written"),
    ("M24", [("    if args.report is not None:\n        run_report(args, parser)",
              "    if args.report is not None:\n        from .report import write_report\n        write_report(peek_board(default_board_path()))\n        run_report(args, parser)")],
     ("TC_4109", ["test_TC_4109_the_source_and_the_readme_pin_the_new_behaviour"]),
     "LLR-4105.1: the CLI reaches the old report again"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(k: str) -> tuple[int, list[str], str]:
    env = {k2: v for k2, v in os.environ.items() if k2 != "NO_COLOR"}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TASKBOARD_REQUIRE_BROWSER="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", T, "-k", k, "-q", "-p", "no:cacheprovider", "-rf"],
                          cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    out = proc.stdout + proc.stderr
    failed = re.findall(r"^FAILED \S+::(\S+)", out, flags=re.M)
    tail = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
    return proc.returncode, failed, tail[-1] if tail else out[-300:]


def main() -> int:
    only = set(sys.argv[1:])
    original = MAIN.read_bytes()
    before = sha(MAIN)
    print(f"{MAIN.name} sha256 before: {before}")
    code, failed, tail = run("report")
    print(f"BASELINE (-k report): exit {code}, failed {failed or 'none'} | {tail}")
    if code != 0:
        print("baseline not green: stop")
        return 2
    killed = survived = 0
    had_reports = (ROOT / "reports").exists()
    for mid, edits, (k, names), what in MUTANTS:
        if only and mid not in only:
            continue
        text = original.decode("utf-8")
        for old, new in edits:
            assert text.count(old) == 1, (mid, old[:60], text.count(old))
            text = text.replace(old, new)
        MAIN.write_bytes(text.encode("utf-8"))
        try:
            code, failed, tail = run(k)
        finally:
            MAIN.write_bytes(original)
            stray = ROOT / "reports"             # a mutant that writes beside the CWD
            if stray.exists() and not had_reports:
                shutil.rmtree(stray)
        hit = [n for n in names if any(f.startswith(n.split("[")[0]) for f in failed)]
        verdict = "KILLED" if code != 0 and hit else "SURVIVED"
        killed += verdict == "KILLED"
        survived += verdict == "SURVIVED"
        print(f"{mid} {verdict}: {what}\n    -k {k!r}: exit {code}, red {failed[:4] or 'none'} | {tail}")
    after = sha(MAIN)
    print(f"{MAIN.name} sha256 after restore: {after} ({'IDENTICAL' if after == before else 'DIFFERENT'})")
    print(f"killed {killed}, survived {survived}")
    return 0 if survived == 0 and after == before else 1


if __name__ == "__main__":
    sys.exit(main())
