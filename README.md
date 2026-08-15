# Indian Market Weekly Sector Screener

Ranks Indian equity sectors by how they performed over the past trading week, and
lists the best-performing shares inside each one. Generates a self-contained HTML
page — two charts, a full sector table, per-sector leaders, and the week's biggest
movers across the whole universe.

Covers **277 NSE/BSE-listed stocks across 21 sectors**, plus five benchmark
indices (Nifty 50, Sensex, Nifty 500, Midcap 50, Smallcap 250).

---

## Download and run

**Requirements:** Python **3.8 or newer** and git. Nothing else — the project uses
only the Python standard library, so there is **no `pip install` step** and no
virtualenv to set up.

Check your Python first:

```bash
python3 --version
```

### 1. Clone the repository

```bash
git clone https://github.com/Ishaan3H/india-sector-screener.git
```

> **This repository is private.** Cloning it requires a GitHub account that has
> been granted access (Settings → Collaborators), and that account must be
> authenticated — either signed in via the [GitHub CLI](https://cli.github.com)
> (`gh auth login`, then `gh repo clone Ishaan3H/india-sector-screener`) or using
> a personal access token / SSH key. Without access the clone fails with
> `repository not found`. If you'd rather not deal with credentials, download the
> ZIP from the repo's green **Code** button and unzip it instead.

### 2. Enter the folder

```bash
cd india-sector-screener
```

### 3. Generate the screener

On **macOS or Linux**:

```bash
./run_weekly.sh
```

On **Windows** (PowerShell or Command Prompt), run the two steps directly:

```bash
python screener.py
python render.py
```

Either route takes about 30 seconds — it downloads ~278 daily price series from
Yahoo Finance and writes `data.json`, then renders `index.html`.

### 4. Open the page

```bash
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

Or just double-click `index.html` in your file manager. It's a single
self-contained file — no server, no internet connection needed to view it.

### What you should see

The script prints the week it computed and the leading sectors before it finishes:

```
[2026-08-15 15:37:33] fetching prices ...
resolving 278 constituents ...
  resolved 277, unresolved 1: ['GUJGASLTD']
wrote data.json: week 2026-08-10 -> 2026-08-14, 21 sectors, 277 stocks
[2026-08-15 15:38:02] rendering page ...

Week 2026-08-10 -> 2026-08-14 (baseline 2026-08-07), 277 stocks
  1. Defence                    +2.08%  best BDL +8.0%
  2. Telecom                    +1.51%  best IDEA +10.8%
  3. Retail & Consumption       +1.02%  best PAYTM +11.2%
```

One or two names in `unresolved` is normal. Many is not — see
[Maintenance](#maintenance).

---

## Refreshing it every week

Run `./run_weekly.sh` again whenever you want fresh numbers. Each run overwrites
`data.json` and `index.html` with the latest completed trading week.

The natural cadence is **Saturday morning IST**, once Friday's 15:30 IST close has
settled. To automate that:

**macOS / Linux — cron.** Run `crontab -e` and add (use your own absolute path):

```bash
0 9 * * 6 /full/path/to/india-sector-screener/run_weekly.sh >> /tmp/screener.log 2>&1
```

**Windows — Task Scheduler.** Create a weekly task for Saturday 09:00 whose
action runs `python` with argument `screener.py`, starting in the project folder;
add a second action for `render.py`.

`data.json` is only overwritten on a successful fetch, so a failed run leaves the
previous week's page intact rather than blanking it.

---

## How performance is measured

- **The week** is the ISO week containing the most recent available close. A
  stock's weekly return compares its last close that week against its last close
  the previous week. Both dates are printed on the page itself, so the window is
  never ambiguous — e.g. *"measured from the Fri 7 Aug close to the Fri 14 Aug
  close."*
- **A sector's return is the median of its constituents' weekly returns** —
  equal-weighted, so no single index heavyweight defines the sector, and robust
  to one outlier blowing up. **Breadth** (the share of constituents that rose) is
  shown next to it, because a median alone can't tell a broad move from a narrow
  one: `+2.08%` on 8 of 12 advancing means something different from the same
  number on 2 of 12.
- Yahoo's own NSE sectoral indices (`^CNXAUTO`, `^CNXFMCG`, …) are deliberately
  **not** used — several publish erratically and were a full month stale when
  this was built, which would have silently shown old data. Sectors are computed
  bottom-up from constituents instead, which also yields the per-sector leaders
  directly.

---

## Files

| File | Purpose |
|---|---|
| `universe.py` | Sector → constituent ticker map, and the benchmark indices |
| `screener.py` | Fetches prices, computes returns, writes `data.json` |
| `render.py` | Turns `data.json` into `index.html` (charts are hand-built inline SVG) |
| `run_weekly.sh` | Driver: fetch → render → print summary |
| `validate_tickers.py` | Checks every ticker still resolves and is fresh |
| `data.json` | Generated — the computed dataset for one week |
| `index.html` | Generated — the screener page |

Adding a sector, or a stock to an existing one, means editing the `SECTORS` dict
in `universe.py` and re-running. Entries are bare NSE roots (`RELIANCE`, not
`RELIANCE.NS`); the fetcher appends `.NS` and falls back to `.BO`.

---

## Maintenance

The one thing that reliably breaks over time is **tickers**, when a company
renames, merges or demerges. Yahoo dropped `TATAMOTORS` after its demerger, and
`LTIM` and `TV18BRDCST` vanished entirely — all three had to be re-pointed.

**Symptom:** `universe_size` falls in `data.json`, or names pile up in
`unresolved`.

**Diagnosis:**

```bash
python3 validate_tickers.py
```

This prints every ticker that fails to resolve or has gone stale. Fix the symbol
in `universe.py` and re-run.

---

## Caveats

- Prices are Yahoo Finance daily closes, **unadjusted for corporate actions** — a
  stock trading ex-dividend, ex-split or ex-bonus during the week will show a
  distorted return. Worth checking before trusting an unusual outlier.
- Sectors overlap where the market does: PSU banks are also banks.
- Individual stock coverage is NSE-first (falling back to BSE); index-level
  coverage spans both exchanges. Yahoo has no usable BSE *sectoral* index series.
- Gain/loss colours are validated for colour-vision deficiency, but no red-green
  pair fully clears the gate in dark mode. Polarity is therefore also carried by
  bar direction, a signed label on every bar, rank order, and the tables — colour
  never carries the sign alone.
- Yahoo Finance is an undocumented endpoint with no uptime guarantee. This is a
  personal research tool, not production infrastructure.
- **Not investment advice.**
