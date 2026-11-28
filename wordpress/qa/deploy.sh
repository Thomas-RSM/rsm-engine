#!/bin/bash
# deploy.sh [plugin] [theme] [home]  -> installs the built ZIPs on the live site and/or republishes pages from site.json
B=https://relevantsearchmedia.com/wp-json; D="$(dirname "$0")/../dist"; S="$(dirname "$0")/../rsm-theme/import/site.json"; T=$(mktemp)
up(){ curl -s -m 300 -X POST "$B/wp/v2/media" -H "Content-Disposition: attachment; filename=$1" -H "Content-Type: application/zip" --data-binary @$D/$1 | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('id') or d)"; }
for a in "$@"; do case $a in
 plugin) P=$(up rsm-elements.zip); echo "plugin: $(curl -s -m 300 -X POST "$B/rsm/v1/deploy" -H 'Content-Type: application/json' -d "{\"media\":$P,\"kind\":\"plugin\"}" | cut -c1-100)";;
 theme) P=$(up rsm-theme.zip); echo "theme: $(curl -s -m 300 -X POST "$B/rsm/v1/deploy" -H 'Content-Type: application/json' -d "{\"media\":$P,\"kind\":\"theme\"}" | cut -c1-100)";;
 site) python3 -I -c "import json,sys;s=json.load(open('$S'));json.dump({'pages':[p for p in s['pages'] if p.get('front')],'llms':s['llms'],'schema_graph':s['schema_graph'],'overwrite':True},open('$T','w'))"; echo "site: $(curl -s -m 300 -X POST "$B/rsm/v1/push" -H 'Content-Type: application/json' --data-binary @$T | cut -c1-260)";;
 *) python3 -I -c "import json,sys;s=json.load(open('$S'));ps=[p for p in s['pages'] if p['key']=='$a'];assert ps,'no such page';json.dump({'pages':ps,'overwrite':True},open('$T','w'))" && echo "$a: $(curl -s -m 300 -X POST "$B/rsm/v1/push" -H 'Content-Type: application/json' --data-binary @$T | cut -c1-260)";;
esac; done
# warm the cache for every page, twice, so no visitor meets a cold one
for n in 1 2; do for l in $(curl -s -m 30 https://relevantsearchmedia.com/sitemap.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//'); do curl -s -o /dev/null -m 40 -H 'Accept-Encoding: br, gzip' "$l"; done; done
curl -s -m 30 "$B/rsm/v1/state?nc=$RANDOM" | python3 -c "import sys,json;d=json.load(sys.stdin);print('live: plugin',d.get('version'),'theme',d.get('theme'),'pages',len([x for x in d['docs'] if x['type']=='page' and x['status']=='publish']))"
