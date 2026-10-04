"""Write evidence/mutants_inc002_r2.json: increment 002 revision 2's battery (the r1
battery with moved anchors, N4 retired with its dead code, and the revision's new
guards)."""
import json
from pathlib import Path

E = Path(__file__).resolve().parent
r1 = json.loads((E / "mutants_inc002.json").read_text(encoding="utf-8"))
keep = [m for m in r1 if m["id"] not in ("N4", "N7", "N8")]
CB, SF = "tests/test_control_bytes.py", "tests/test_sync_fields.py"
AT407 = "tests/test_markup_sites.py::test_AT_407_a_shared_config_cannot_act_or_crash"
new = [
 ("N7", "taskboard/models.py", 'raw = clean_strings(json.loads(path.read_text(encoding="utf-8")))',
  'raw = json.loads(path.read_text(encoding="utf-8"))', [CB], "the load door is open"),
 ("N8", "taskboard/team_sync.py", 'data = clean_strings(json.loads(path.read_text(encoding="utf-8")))',
  'data = json.loads(path.read_text(encoding="utf-8"))', [CB], "the sync door is open"),
 ("R1", "taskboard/team_sync.py", "if not isinstance(pid, str) or not pid or pid in seen:",
  "if not isinstance(pid, str) or pid in seen:", [SF], "an empty synced id is accepted (F1: the board grows per tick)"),
 ("R2", "taskboard/team_sync.py", "except (OSError, json.JSONDecodeError, TypeError, ValueError, RecursionError):",
  "except (OSError, json.JSONDecodeError, TypeError, ValueError):", [CB], "the sync door lets a deep file raise (S4-1)"),
 ("R3", "taskboard/models.py", "except (json.JSONDecodeError, OSError, TypeError, ValueError, RecursionError):",
  "except (json.JSONDecodeError, OSError, TypeError, ValueError):", [CB], "the load door lets a deep file raise (S4-1)"),
 ("R4", "taskboard/app.py", "if (not self.team_state.load_config()",
  "if (self.team_state.load_config() and False", [CB], "an unreadable team.json is silent (S4-1: no visible error)"),
 ("R5", "taskboard/app.py", 'team_projects.setdefault(p["id"], p)     # the first entry of an id wins',
  'team_projects[p["id"]] = p', [SF], "Setup keeps the last duplicate (F3)"),
 ("R6", "taskboard/app.py",
  '"name": proj.name,\n                    "color": proj.color,\n                    "status": proj.status,\n                    "template": template if isinstance(template, str) else "",',
  '"name": team_projects[proj.id].get("name", proj.name),\n                    "color": team_projects[proj.id].get("color", proj.color),\n                    "status": team_projects[proj.id].get("status", proj.status),\n                    "template": team_projects[proj.id].get("template", ""),',
  [SF], "Setup republishes the raw synced fields (F3)"),
 ("R7", "taskboard/models.py", 'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0',
  'if c in "\t" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0', [CB], "the rule also drops newline (F2 mutA)"),
 ("R8", "taskboard/models.py", 'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0',
  'if c in "\t\n" or 0x20 <= ord(c) < 0x7f', [CB], "the rule drops every character from U+00A0 (F2 mutB)"),
]
out = keep + [{"id": i, "file": f, "old": o, "new": n, "nodes": nodes, "why": w}
              for i, f, o, n, nodes, w in new]
(E / "mutants_inc002_r2.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
print(len(out), sorted(m["id"] for m in out))
