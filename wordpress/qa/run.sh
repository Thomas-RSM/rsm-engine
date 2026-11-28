#!/bin/bash
# run.sh /path/  -> runs the gate for a page using the facts recorded in pages.py
cd "$(dirname "$0")"; python3 -I - "$1" <<'PY'
import sys, os, subprocess
import json
g = json.load(open('gate-pages.json'))[sys.argv[1]]
sys.exit(subprocess.call([sys.executable, '-I', 'gate.py', sys.argv[1], '--keywords', g['kw'] or ';', '--type', g['type'], '--example', g['example'], '--original', g['original']] + (['--trade', g['trade']] if g.get('trade') else [])))
PY
