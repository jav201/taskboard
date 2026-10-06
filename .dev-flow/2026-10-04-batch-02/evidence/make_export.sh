#!/usr/bin/env bash
# Scratch EXPORT for the mutation battery (C-40: never mutate the working tree).
#   bash make_export.sh <repo> <dest>
# `git archive HEAD` of <repo>, then the working tree's taskboard/ and tests/ copied over it
# (the increment's uncommitted bytes), bytecode caches excluded.
set -euo pipefail
REPO="$1"; DEST="$2"
rm -rf "$DEST"; mkdir -p "$DEST"
git -C "$REPO" archive HEAD | tar -x -C "$DEST"
for d in taskboard tests; do
  (cd "$REPO" && find "$d" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' -print0) |
    while IFS= read -r -d '' f; do mkdir -p "$DEST/$(dirname "$f")"; cp "$REPO/$f" "$DEST/$f"; done
done
echo "export ready: $(basename "$DEST")"
