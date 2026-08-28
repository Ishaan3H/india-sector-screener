"""Refuse to publish a bad dataset.

Run after screener.py. Exits non-zero with an explanation if data.json looks
wrong, so an automated refresh fails loudly instead of quietly replacing a good
page with a broken one.
"""

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_UNIVERSE = 240          # normally ~278
MAX_AGE_DAYS = 9            # a Saturday run sees a Friday close; allow for holidays

with open(os.path.join(HERE, "data.json"), encoding="utf-8") as fh:
    d = json.load(fh)

problems = []

end = dt.date.fromisoformat(d["week_end"])
base = dt.date.fromisoformat(d["baseline"])
age = (dt.date.today() - end).days

if age > MAX_AGE_DAYS:
    problems.append(
        f"week_end {end} is {age} days old (limit {MAX_AGE_DAYS}). "
        "Either the market has been shut, or the price source stopped updating."
    )
if not 3 <= (end - base).days <= 12:
    problems.append(
        f"baseline {base} is {(end - base).days} days before week_end {end}; "
        "expected about 7. The week-over-week comparison may be wrong."
    )
if d["universe_size"] < MIN_UNIVERSE:
    problems.append(
        f"only {d['universe_size']} stocks resolved (expected >= {MIN_UNIVERSE}). "
        f"Unresolved: {', '.join(d['unresolved']) or 'none'}. "
        "Tickers most likely changed - run validate_tickers.py."
    )
if len(d["sectors"]) < 18:
    problems.append(f"only {len(d['sectors'])} sectors built (expected 21).")
if not d.get("benchmarks"):
    problems.append("no benchmark indices resolved.")

if problems:
    print("Output failed its sanity checks - NOT publishing:\n", file=sys.stderr)
    for p in problems:
        print(f"  * {p}", file=sys.stderr)
    sys.exit(1)

print(
    f"OK: week {d['week_start']} -> {d['week_end']} (baseline {d['baseline']}), "
    f"{d['universe_size']} stocks, {len(d['sectors'])} sectors, "
    f"{len(d['benchmarks'])} benchmarks, {age}d old"
)
