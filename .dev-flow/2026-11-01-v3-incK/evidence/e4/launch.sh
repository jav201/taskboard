#!/bin/sh
# Launch one DeepSeek v4 Pro build of an Inc K group. Usage: launch.sh <G>
G=$1
cd /c/Users/jjgh8/Github/taskboard-wt/capture-proto || exit 2
E=.dev-flow/2026-11-01-v3-incK/evidence/e4
rm -f $E/build-$G.done
timeout 3600 pi -p --no-session --model deepseek/deepseek-v4-pro "You are an implementer. Read and follow the task file .dev-flow/2026-11-01-v3-incK/e4-task-$G.md in the current directory exactly. Use the interpreter C:/Users/jjgh8/anaconda3/python.exe for every Python command." < /dev/null > $E/build-$G.log 2>&1
echo "EXIT $? $(date -u +%FT%TZ)" > $E/build-$G.done
