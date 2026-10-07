"""Rollover 2026-10-04-batch-02 -> B2b (2026-10-06-batch-01), per
stations/shared-batch.md §Batch rollover. Uses devflow-init.py's own template
helpers so the seeded record is byte-faithful to what init would write."""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

ROOT = r"C:\Users\jjgh8\Github\taskboard\.claude\worktrees\present-e"
BUNDLE = r"C:\Users\jjgh8\.claude\skills\dev-flow"
TODAY = "2026-10-07"
OUTGOING = "2026-10-07-batch-02"
OBJECTIVE = ("Batch E of the kg_mejoras plan: the presentation mode behind R (replacing the "
             "report) -- the PRES-C interactive hybrid per the operator's verdict 2026-10-07 "
             "(gantt on top, brief blocks below, a ⟦━⟧ cursor expanding the notes), exporting "
             "SVG and PNG")

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
    # the interrupted first rollover attempt wrote it before crashing -- accept it
    # only if it holds the outgoing log verbatim
    with open(archive, encoding="utf-8") as fh:
        assert json.load(fh) == doc["decisions_log"], "archive disagrees with the log"
else:
    with open(archive, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc["decisions_log"], fh, indent=2, ensure_ascii=False)
        fh.write("\n")

batch = di._batch_id(ROOT, TODAY)
assert batch == "2026-10-07-batch-03", batch  # renamed to -batch-04 below (main holds -03 uncommitted)

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
    "Operator (Javier), 2026-10-07: the presentation prototype's verdict (PRES-C the interactive "
    "hybrid; SVG + PNG export; R replaces the report) + 'HAz ambas, paraleliza'. Read with the "
    "established chain: autonomous gates with the two exceptions; the COORDINATOR merges/commits "
    "from the worktree after the gates (no PR); synthetic boards only.")

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
