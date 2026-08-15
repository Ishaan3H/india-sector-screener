#!/bin/bash
# Rebuild the Indian market weekly sector screener.
#
#   ./run_weekly.sh
#
# Fetches fresh prices, recomputes the sector table, and regenerates index.html.
# data.json is only overwritten on a successful fetch, so a failed run leaves the
# previous week's page intact rather than blanking it.
set -euo pipefail

cd "$(dirname "$0")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] fetching prices ..."
python3 screener.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] rendering page ..."
python3 render.py

python3 - <<'PY'
import json
d = json.load(open("data.json"))
top = d["sectors"][:3]
print(f"\nWeek {d['week_start']} -> {d['week_end']} (baseline {d['baseline']}), "
      f"{d['universe_size']} stocks")
for i, s in enumerate(top, 1):
    print(f"  {i}. {s['sector']:26} {s['week']:+6.2f}%  best {s['best']} {s['best_week']:+.1f}%")
PY

echo "[$(date '+%Y-%m-%d %H:%M:%S')] done -> $(pwd)/index.html"
