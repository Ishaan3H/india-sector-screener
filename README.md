# Indian Market Weekly Sector Screener

Ranks Indian equity sectors by how they performed over the past trading week, and
lists the best-performing shares inside each one. Generates a self-contained HTML
page — two charts, a full sector table, per-sector leaders, and the week's biggest
movers across the whole universe.

Covers **277 NSE/BSE-listed stocks across 21 sectors**, plus five benchmark
indices (Nifty 50, Sensex, Nifty 500, Midcap 50, Smallcap 250).

---

## Download and run

**The only requirement is Python 3.8 or newer.** The project uses nothing but the
Python standard library, so there is **no `pip install` step**, no virtualenv, and
no other dependencies.

Pick your platform:

- [Windows](#windows)
- [macOS / Linux](#macos--linux)

---

### Windows

#### 1. Install Python

Skip this if you already have it — open **PowerShell** (press <kbd>Win</kbd>, type
`powershell`, hit Enter) and check:

```powershell
py --version
```

If that prints something like `Python 3.12.1`, you're set. If it says the term is
not recognized, install Python either way:

- **Easiest:** download the installer from
  [python.org/downloads/windows](https://www.python.org/downloads/windows/) and run it.
  On the first screen, **tick "Add python.exe to PATH"** before clicking Install —
  this is the single most common thing people miss, and skipping it is why
  `python` later comes back "not recognized".
- **Or via winget:** `winget install Python.Python.3.12`

Close and reopen PowerShell afterwards, then re-run `py --version` to confirm.

> **Note:** use `py` rather than `python` on Windows. Typing `python` can open the
> Microsoft Store instead of running anything, because Windows ships a placeholder
> by that name. `py` is the official Python launcher and always points at your real
> install.

#### 2. Download the project

**Without git — recommended if you don't already use it:**

1. Go to <https://github.com/Ishaan3H/india-sector-screener>
2. Click the green **Code** button → **Download ZIP**
3. Open your Downloads folder, right-click `india-sector-screener-main.zip` →
   **Extract All…** → **Extract**

**With git,** if you have [Git for Windows](https://git-scm.com/download/win):

```powershell
git clone https://github.com/Ishaan3H/india-sector-screener.git
```

#### 3. Open PowerShell in that folder

In File Explorer, open the extracted folder (the one containing `screener.py`),
then hold <kbd>Shift</kbd>, right-click any empty space inside it, and choose
**Open PowerShell window here**. Or `cd` to it manually:

```powershell
cd $HOME\Downloads\india-sector-screener-main
```

#### 4. Generate the screener

```powershell
.\run_weekly.bat
```

If PowerShell blocks the script, run the two steps directly instead — this always
works:

```powershell
py screener.py
py render.py
```

#### 5. Open the page

```powershell
start index.html
```

Or just double-click `index.html` in File Explorer.

---

### macOS / Linux

macOS ships with Python 3; most Linux distributions do too. Check with
`python3 --version`, and install from [python.org](https://www.python.org/downloads/)
or your package manager if it's missing.

```bash
git clone https://github.com/Ishaan3H/india-sector-screener.git
cd india-sector-screener
./run_weekly.sh
open index.html          # macOS
xdg-open index.html      # Linux
```

No account or credentials needed to clone. If you'd rather not use git, download
the ZIP from the green **Code** button and unzip it instead.

---

### What to expect

The fetch takes about 30 seconds — it downloads ~278 daily price series from Yahoo
Finance, writes `data.json`, then renders `index.html`. You need an internet
connection for that step, but not to view the finished page: `index.html` is one
self-contained file with no server and no external assets.

The script prints the week it computed and the leading sectors before it finishes:

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

Run the same command again whenever you want fresh numbers — `.\run_weekly.bat` on
Windows, `./run_weekly.sh` on macOS/Linux. Each run overwrites `data.json` and
`index.html` with the latest completed trading week.

The natural cadence is **Saturday morning IST**, once Friday's 15:30 IST close has
settled. To automate that:

**macOS / Linux — cron.** Run `crontab -e` and add (use your own absolute path):

```bash
0 9 * * 6 /full/path/to/india-sector-screener/run_weekly.sh >> /tmp/screener.log 2>&1
```

**Windows — Task Scheduler.** Press <kbd>Win</kbd> and open **Task Scheduler**, then
**Create Basic Task…**:

1. Name it anything, e.g. *India sector screener*
2. Trigger: **Weekly** → tick **Saturday** → start time `09:00`
3. Action: **Start a program**
4. Program/script: browse to `run_weekly.bat` in the project folder
5. **Start in (optional):** set this to the project folder path — leave it blank
   and the task runs from `system32`, where it won't find the scripts

Tick *"Open the Properties dialog"* at the end if you also want *"Run whether user
is logged on or not."*

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
| `run_weekly.sh` | Driver for macOS/Linux: fetch → render → print summary |
| `run_weekly.bat` | Same driver for Windows |
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
