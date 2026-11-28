#!/bin/bash
# run.sh /path/  -> runs the gate for a page using the facts recorded in pages.py
cd "$(dirname "$0")"; python3 -I - "$1" <<'PY'
import sys, os, subprocess
sys.path.insert(0, os.path.join(os.getcwd(), '..'))
import pages
g = pages.GATE[sys.argv[1]]
sys.exit(subprocess.call([sys.executable, '-I', 'gate.py', sys.argv[1], '--keywords', g['kw'], '--type', g['type'], '--example', g['example'], '--original', g['original']] + (['--trade', g['trade']] if g.get('trade') else [])))
PY
