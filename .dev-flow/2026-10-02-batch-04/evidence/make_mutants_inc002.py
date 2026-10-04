"""Write evidence/mutants_inc002.json (increment 002's battery)."""
import json
from pathlib import Path

CB = "tests/test_control_bytes.py"
SF = "tests/test_sync_fields.py"
AT407 = "tests/test_markup_sites.py::test_AT_407_a_shared_config_cannot_act_or_crash"
M = [
 ("N1", "taskboard/models.py", r'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0',
  r'if c in "\t\n\r" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0', [CB], "the rule keeps CR"),
 ("N2", "taskboard/models.py", r'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0',
  r'if c in "\t\n" or 0x20 <= ord(c) <= 0x7f or ord(c) >= 0xa0', [CB], "the rule keeps DEL"),
 ("N3", "taskboard/models.py", r'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0',
  r'if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) > 0xa0', [CB], "the rule drops NBSP"),
 ("N4", "taskboard/models.py", r'return "".join(c for c in value.replace("\r\n", "\n")',
  r'return "".join(c for c in value', [CB], "CR-LF is not turned into a newline (the CR is dropped, the pair joins)"),
 ("N5", "taskboard/models.py", "return {strip_controls(k): clean_strings(v) for k, v in value.items()}",
  "return {k: clean_strings(v) for k, v in value.items()}", [CB], "keys are not cleaned"),
 ("N6", "taskboard/models.py", "return strip_controls(text)[:_MAX_PASTE_CHARS] or None",
  "return text[:_MAX_PASTE_CHARS] or None", [CB, "tests/test_app.py::test_clean_clipboard_text_strips_controls_and_caps"],
  "the clipboard bypasses the rule"),
 ("N7", "taskboard/models.py", "raw = clean_strings(raw)        # the load door: no control byte gets in",
  "pass", [CB], "the load door is open"),
 ("N8", "taskboard/team_sync.py", "return clean_strings(data) if isinstance(data, dict) else None",
  "return data if isinstance(data, dict) else None", [CB], "the sync door is open"),
 ("N9", "taskboard/models.py", "if not isinstance(color, str):         # a synced or hand-edited value of",
  "if False:", [SF, AT407], "an unhashable colour reaches the dict lookup (S2-2)"),
 ("N10", "taskboard/models.py", 'name=name if isinstance(name, str) and name else "Untitled",',
  'name=name if name is not None else "Untitled",', [SF, CB], "a non-text name loads raw"),
 ("N11", "taskboard/models.py", 'archived=d.get("archived") is True,',
  'archived=bool(d.get("archived", False)),', [SF, CB], "a truthy non-boolean flag archives"),
 ("N12", "taskboard/models.py", "due_date=due if isinstance(due, str) else None,",
  "due_date=due,", [SF, CB], "a non-text date loads raw"),
 ("N13", "taskboard/team_sync.py", "if not isinstance(pid, str) or pid in seen:",
  "if not isinstance(pid, str):", [SF, AT407], "a later entry of the same id is applied (S3-1)"),
 ("N14", "taskboard/team_sync.py", 'if key == "name" and not (isinstance(value, str) and value):',
  "if False:", [SF, AT407], "a refused synced name overwrites with Untitled"),
 ("N15", "taskboard/team_sync.py", 'if key.endswith("_date") and not (value is None or isinstance(value, str)):',
  "if False:", [SF, AT407], "a refused synced date clears the date"),
 ("N16", "taskboard/team_sync.py", "if key not in pd:", "if False:", [SF],
  "absent keys are applied with the loading defaults (A2-1)"),
 ("N17", "taskboard/team_sync.py", "setattr(existing, key, getattr(fresh, key))",
  "setattr(existing, key, pd[key])", [SF, AT407], "the raw synced value is applied (S-1's seat)"),
 ("N18", "taskboard/team_sync.py", '"hue": hue if isinstance(hue, str) and hue in HEX else "mut"})',
  '"hue": hue})', [SF, AT407], "a roster hue outside the palette reaches the views"),
 ("N19", "taskboard/team_sync.py", 'out.append({**r, "name": name if isinstance(name, str) and name else r["id"],',
  'out.append({**r, "name": name,', [SF, AT407], "a non-text roster name reaches the views"),
 ("N20", "taskboard/team_sync.py", 'if not (isinstance(r, dict) and isinstance(r.get("id"), str)) or r["id"] in seen:',
  'if not (isinstance(r, dict) and isinstance(r.get("id"), str)):', [SF, AT407], "duplicate roster ids kept"),
 ("N21", "taskboard/team_sync.py", 'return clean_roster(self.config.get("roster", []))',
  'return [r for r in self.config.get("roster", []) if isinstance(r, dict) and isinstance(r.get("id"), str)]',
  [SF, AT407], "roster() bypasses the cleaner"),
 ("N22", "taskboard/app.py", 'for r in clean_roster(cfg.get("roster", []))]',
  'for r in cfg.get("roster", []) if isinstance(r, dict) and isinstance(r.get("hue", "mut"), str) and isinstance(r.get("name"), str)]',
  [AT407], "the Setup view's roster bypasses the cleaner (A3-1)"),
 ("N23", "taskboard/app.py", "existing = _read_json(team_json_path)",
  'existing = __import__("json").loads(team_json_path.read_text(encoding="utf-8")) if team_json_path.exists() else None',
  [CB], "the Setup view's team.json read bypasses the sync door (A-3)"),
]
out = [{"id": i, "file": f, "old": o, "new": n, "nodes": nodes, "why": why}
       for i, f, o, n, nodes, why in M]
(Path(__file__).resolve().parent / "mutants_inc002.json").write_text(
    json.dumps(out, indent=1) + "\n", encoding="utf-8")
print(len(out))
