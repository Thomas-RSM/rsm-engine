#!/bin/bash
# all.sh -> gate every live page, one line each. Use after any shared change.
cd "$(dirname "$0")"
echo "/ : $(python3 -I gate.py / --keywords 'seo company in usa;seo agency in usa;seo company' --type home 2>&1 | grep -E '^FAIL|^  FAIL|^GATE' | tr '\n' ' ' | cut -c1-400)"
for u in $(python3 -I -c "import json;print(' '.join(json.load(open('gate-pages.json'))))"); do echo "$u : $(./run.sh $u 2>&1 | grep -E '^FAIL|^  FAIL|^GATE' | tr '\n' ' ' | cut -c1-400)"; done
python3 -I records.py
