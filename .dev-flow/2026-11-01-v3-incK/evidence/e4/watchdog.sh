#!/bin/sh
# Stall watchdog for long background jobs: prints a line when the watched log
# and the watched source files have not changed for $3 seconds, and when the
# job's done-marker appears. Usage: watchdog.sh <log> <donefile> <stall_s> <files...>
log=$1; done=$2; stall=$3; shift 3
last=""; quiet=0
while [ ! -f "$done" ]; do
  sig=$(stat -c '%s %Y' "$log" "$@" 2>/dev/null | md5sum)
  if [ "$sig" = "$last" ]; then quiet=$((quiet+30)); else quiet=0; last=$sig; fi
  if [ $quiet -ge $stall ]; then echo "STALL: no change in $log or sources for ${quiet}s"; quiet=0; fi
  sleep 30
done
echo "DONE: $(cat "$done")"
