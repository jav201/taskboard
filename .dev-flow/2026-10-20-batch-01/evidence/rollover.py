"""Rollover 2026-10-19-batch-01 -> 2026-10-20-batch-01 (stations/shared-batch.md §Batch rollover),
with devflow-init.py's own seed helpers (the 2026-10-18/19 pattern)."""
import datetime, importlib.util, json, os, subprocess
ROOT = r"C:\Users\jjgh8\Github\taskboard"
BUNDLE = r"C:\Users\jjgh8\.claude\skills\dev-flow"
TODAY = "2026-10-20"
OUTGOING = "2026-10-19-batch-01"
BATCH = "2026-10-20-batch-01"
OBJECTIVE = ("Multi-board (variant C, home cards, of the multi-board round): several boards in one "
             "taskboard -- a boards registry with one folder per board and today's board as `Main` "
             "in place, the active board's chip in the head row, the Home cards behind `B` (shown at "
             "launch when more than one board is open), create / rename+recolour / archive boards, "
             "`--board PATH` registering its board, and moving a project to another board from the "
             "projects modal (backups, a move log, crossing links dropped and logged, team mode refused)")
spec = importlib.util.spec_from_file_location("devflow_init", os.path.join(BUNDLE, "scripts", "devflow-init.py"))
di = importlib.util.module_from_spec(spec); spec.loader.exec_module(di)
state_path = os.path.join(ROOT, ".dev-flow", "state.json")
doc = json.loads(open(state_path, encoding="utf-8").read())
assert doc["batch_id"] == OUTGOING and doc["phase_status"] == "closed"
archive = os.path.join(ROOT, ".dev-flow", OUTGOING, "decisions-log.json")
assert not os.path.exists(archive)
with open(archive, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc["decisions_log"], fh, indent=2, ensure_ascii=False); fh.write("\n")
batch = di._batch_id(ROOT, TODAY)
assert batch == BATCH, batch
git = lambda *a: subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True).stdout.strip()
base_ref = git("rev-parse", "HEAD")
owner = git("rev-parse", "--show-toplevel")
found = di._found(ROOT)
homes = {k: v.replace("<batch_id>", batch).replace("<project>", doc["project"]) for k, v in di.ARTIFACT_HOMES}
doc.update({
    "batch_id": batch, "batch_objective": OBJECTIVE, "owner": owner,
    "current_station": "P0", "phase_status": "not-started",
    "stations_active": ["P0", "P1", "P2", "P3", "P4", "P5"],
    "iterations_per_station": {s: 0 for s in ["P0", "P1", "P2", "P3", "P4", "P5"]},
    "triggers": {"evaluated_at": None, "fired": [], "not_fired": [], "record": di.TRIGGERS_RECORD},
    "artifact_homes": homes, "base_ref": base_ref, "artifacts": {}, "decisions_log": [],
    "obsidian_synced": False, "created_at": datetime.datetime.now().isoformat(),
})
doc.pop("standing_authorization", None)
doc["mode"] = "core"
doc["mode_history"].append({"from": None, "to": "core", "date": TODAY,
    "reason": "batch %s opened by rollover from %s; mode core declared by the commission" % (batch, OUTGOING)})
with open(state_path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc, fh, indent=2, ensure_ascii=False); fh.write("\n")
flow = di._flow_home()
bdir = os.path.join(ROOT, ".dev-flow", batch)
os.makedirs(bdir)
req = di._template(flow, "req-template.md")
ledger = di._ledger_seed(req)
written = []
for name, dest in di.SEEDS:
    text = di._template(flow, name)
    text = text.replace("<PROJECT>", doc["project"]).replace("<BATCH_ID>", batch).replace("<YYYY-MM-DD>", TODAY)
    if dest == "PLAN.md":
        text = text.replace(di.OBJECTIVE_TOKEN, OBJECTIVE)
    if di.FOUND_LABEL in text:
        text = di._fill_found(text, found)
    p = os.path.join(bdir, dest); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    written.append(dest)
with open(os.path.join(bdir, "01-requirements-ledger.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(ledger.replace("<PROJECT>", doc["project"]).replace("<BATCH_ID>", batch).replace("<YYYY-MM-DD>", TODAY))
written.append("01-requirements-ledger.md")
os.makedirs(os.path.join(bdir, "03-increments"), exist_ok=True)
os.makedirs(os.path.join(bdir, "evidence"), exist_ok=True)
packet = di._template(flow, di.PACKET_SEED[0])
packet = "\n".join((line.replace("<batch_id>", batch).replace("<NNN>", di.PACKET_SEED[2]).replace("<YYYY-MM-DD>", TODAY)
                    if line.startswith(di.PACKET_HEADER_LINES) else line)
                   for line in packet.split("\n") if not line.startswith(di.PACKET_EXAMPLE_ROW))
with open(os.path.join(bdir, "03-increments", di.PACKET_SEED[1]), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(packet)
written.append("03-increments/" + di.PACKET_SEED[1])
with open(os.path.join(bdir, "evidence", ".gitattributes"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("** -text\n")
print("batch:", batch); print("base_ref:", base_ref); print("seeded:", ", ".join(sorted(written)))
print("found:", [n for n, _ in found] or "none")
