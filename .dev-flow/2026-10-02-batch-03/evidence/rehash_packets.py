"""Re-computes the SHA-256 cell of every evidence row in this batch's increment
packets (`| label | `<path>` | `<64-hex>` |`) from the bytes now at that path.
Run after any evidence file is rewritten (e.g. re-redacted). Prints each change."""
import hashlib
import re
from pathlib import Path

batch = Path(__file__).resolve().parents[1]
root = batch.parents[1]
row = re.compile(r"^(\| [^|]+ \| `)([^`]+)(` \| `)([0-9a-f]{64})(` \|)$")
for packet in sorted((batch / "03-increments").glob("increment-*.md")):
    lines = packet.read_text(encoding="utf-8").split("\n")
    for i, line in enumerate(lines):
        m = row.match(line)
        if not m:
            continue
        digest = hashlib.sha256((root / m.group(2)).read_bytes()).hexdigest()
        if digest != m.group(4):
            print(f"{packet.name}: {m.group(2)} {m.group(4)[:12]} -> {digest[:12]}")
            lines[i] = m.group(1) + m.group(2) + m.group(3) + digest + m.group(5)
    with open(packet, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
