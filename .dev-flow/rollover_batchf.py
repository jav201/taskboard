"""Rollover 2026-10-07-batch-04 -> batch-05 (the carries batch), per
stations/shared-batch.md §Batch rollover. Uses devflow-init.py's own template
helpers so the seeded record is byte-faithful to what init would write."""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

ROOT = r"C:\Users\jjgh8\Github\taskboard"
BUNDLE = r"C:\Users\jjgh8\.claude\skills\dev-flow"
TODAY = "2026-10-07"
OUTGOING = "2026-10-07-batch-04"
OBJECTIVE = ("Carries batch: close the BACKLOG's standing items -- S5-3 a failed backup write "
             "leaves no partial file (_create_beside unlinks its exclusively created file on a "
             "failed write, a RED arm with a refusing remove); F-6 the Mon D formatter in three "
             "copies becomes one; UXV-3 `u` on a single-task change says what came back (one-line "
             "undo toast); UXV-6 the ? help at 80 cells clips with `...` never mid-word; the "
             "chain-map carries (deep chains fold with a per-band +N more cap, the resize-heal "
             "re-verifies the selection against the fresh line_map, AT-801b's docstring); the "
             "P4 F-3..F-5 test-strength arms; BACKLOG bookkeeping (present-a-project closes "
             "with batch E)")

spec = importlib.util.spec_from_file_location(
    "devflow_init", os.path.join(BUNDLE, "scripts", "devflow-init.py"))
di = importlib.util.module_from_spec(spec)
spec.loader.exec_module(di)

state_path = os.path.join(ROOT, ".dev-flow", "state.json")
doc = json.loads(open(state_path, encoding="utf-8").read())
assert doc["batch_id"] == OUTGOING, doc["batch_id"]
assert doc["phase_status"] == "closed", doc["phase_status"]

# 1. Archive the outgoing decisions_log -- MOVED, never copied.
archive = os.path.join(ROOT, ".dev-flow", OUTGOING, "decisions-log.json")
if os.path.exists(archive):
    with open(archive, encoding="utf-8") as fh:
        assert json.load(fh) == doc["decisions_log"], "archive disagrees with the log"
else:
    with open(archive, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc["decisions_log"], fh, indent=2, ensure_ascii=False)
        fh.write("\n")

batch = di._batch_id(ROOT, TODAY)
assert batch == "2026-10-07-batch-05", batch

def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args),
                          capture_output=True, text=True).stdout.strip()

base_ref = git("rev-parse", "HEAD")
owner = git("rev-parse", "--show-toplevel")
found = di._found(ROOT)

homes = {k: v.replace("<batch_id>", batch).replace("<project>", doc["project"])
         for k, v in di.ARTIFACT_HOMES}

doc.update({
    "batch_id": batch,
    "batch_objective": OBJECTIVE,
    "owner": owner,
    "current_station": "P0",
    "phase_status": "not-started",
    "stations_active": ["P0", "P1", "P2", "P3", "P4", "P5"],
    "iterations_per_station": {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0, "P5": 0},
    "triggers": {"evaluated_at": None, "fired": [], "not_fired": [],
                 "record": di.TRIGGERS_RECORD},
    "artifact_homes": homes,
    "base_ref": base_ref,
    "artifacts": {},
    "decisions_log": [],
    "standing_authorization": {"autonomous": True, "merge": False, "asked_on": TODAY,
                               "operator_words": ""},  # filled below
    "obsidian_synced": False,
    "created_at": datetime.datetime.now().isoformat(),
})
doc["mode"] = "core"
doc["mode_history"].append({
    "from": None, "to": "core", "date": TODAY,
    "reason": "batch %s opened by rollover from %s; mode core declared by the commission"
              % (batch, OUTGOING)})
doc["standing_authorization"]["operator_words"] = (
    "Operator (Javier), 2026-10-07: 'Ok, continuemos' -- continue until the plan's proposed "
    "changes are done; the remaining work is the BACKLOG's standing carries. Read with the "
    "established chain: Gates -- autonomous with the two exceptions; Git -- the COORDINATOR "
    "commits and pushes at each close (no PR); data safeguard -- synthetic boards only; "
    "implementing agents (DeepSeek instances under coordinator briefs, the standing 'Sigue "
    "usando Deepseek') do NOT commit/push/stash. This batch runs in the MAIN checkout.")

with open(state_path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

# 2. Seed the batch record from the flow's templates (init step 4's own logic).
flow = di._flow_home()
bdir = os.path.join(ROOT, ".dev-flow", batch)
os.makedirs(bdir)
req = di._template(flow, "req-template.md")
ledger = di._ledger_seed(req)
written = []
for name, dest in di.SEEDS:
    text = di._template(flow, name)
    text = (text.replace("<PROJECT>", doc["project"]).replace("<BATCH_ID>", batch)
            .replace("<YYYY-MM-DD>", TODAY))
    if dest == "PLAN.md":
        text = text.replace(di.OBJECTIVE_TOKEN, OBJECTIVE)
    if di.FOUND_LABEL in text:
        text = di._fill_found(text, found)
    with open(os.path.join(bdir, dest), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    written.append(dest)
with open(os.path.join(bdir, "01-requirements-ledger.md"), "w", encoding="utf-8",
          newline="\n") as fh:
    fh.write(ledger.replace("<PROJECT>", doc["project"]).replace("<BATCH_ID>", batch)
             .replace("<YYYY-MM-DD>", TODAY))
written.append("01-requirements-ledger.md")
os.makedirs(os.path.join(bdir, "03-increments"))
os.makedirs(os.path.join(bdir, "evidence"))
packet = di._template(flow, di.PACKET_SEED[0])
packet = "\n".join(
    (line.replace("<batch_id>", batch).replace("<NNN>", di.PACKET_SEED[2])
     .replace("<YYYY-MM-DD>", TODAY) if line.startswith(di.PACKET_HEADER_LINES) else line)
    for line in packet.split("\n") if not line.startswith(di.PACKET_EXAMPLE_ROW))
with open(os.path.join(bdir, "03-increments", di.PACKET_SEED[1]), "w", encoding="utf-8",
          newline="\n") as fh:
    fh.write(packet)
written.append("03-increments/" + di.PACKET_SEED[1])

# 3. The evidence home is marked -text (init step 7).
ga = os.path.join(ROOT, ".gitattributes")
mark = ".dev-flow/%s/evidence/** -text" % batch
existing = open(ga, encoding="utf-8", errors="replace").read() if os.path.isfile(ga) else ""
if mark not in existing:
    with open(ga, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(("" if existing.endswith("\n") or not existing else "\n") + mark + "\n")

print("batch:", batch)
print("archived:", os.path.relpath(archive, ROOT), "(%d entries)" % len(json.load(open(archive, encoding='utf-8'))))
print("base_ref:", base_ref)
print("seeded:", ", ".join(sorted(written)))
print("found:", [n for n, _ in found] or "none")
