"""Sector -> constituent universe for the Indian market screener.

Symbols are Yahoo Finance tickers. `.NS` = NSE listing, `.BO` = BSE listing.
The fetcher tries the NSE listing first and falls back to the BSE listing,
so each entry is written as a bare NSE symbol root.

Sector buckets follow the NSE sectoral/thematic index families (Nifty Bank,
Nifty IT, Nifty Auto, ...) but are maintained here as plain constituent lists
because Yahoo's own sectoral index series are updated erratically.
"""

BENCHMARKS = [
    ("^NSEI", "NIFTY 50"),
    ("^BSESN", "BSE SENSEX"),
    ("^CRSLDX", "NIFTY 500"),
    ("^NSEMDCP50", "NIFTY MIDCAP 50"),
    ("NIFTYSMLCAP250.NS", "NIFTY SMALLCAP 250"),
]

SECTORS = {
    "Banks": [
        "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "SBIN", "INDUSINDBK",
        "BANKBARODA", "PNB", "CANBK", "IDFCFIRSTB", "FEDERALBNK", "AUBANK",
        "BANDHANBNK", "RBLBANK", "YESBANK", "INDIANB", "UNIONBANK", "KARURVYSYA",
    ],
    "PSU Banks": [
        "SBIN", "BANKBARODA", "PNB", "CANBK", "UNIONBANK", "INDIANB",
        "BANKINDIA", "CENTRALBK", "UCOBANK", "IOB", "MAHABANK", "PSB", "J&KBANK",
    ],
    "IT": [
        "TCS", "INFY", "HCLTECH", "WIPRO", "TECHM", "PERSISTENT",
        "COFORGE", "MPHASIS", "LTTS", "OFSS", "TATAELXSI", "KPITTECH",
        "CYIENT", "BSOFT", "HAPPSTMNDS", "ZENSARTECH", "SONATSOFTW",
    ],
    "Auto & Ancillaries": [
        "MARUTI", "TMPV", "M&M", "BAJAJ-AUTO", "HEROMOTOCO", "EICHERMOT",
        "TVSMOTOR", "ASHOKLEY", "BHARATFORG", "MOTHERSON", "BOSCHLTD",
        "BALKRISIND", "MRF", "APOLLOTYRE", "EXIDEIND", "TIINDIA", "SONACOMS",
        "ENDURANCE",
    ],
    "Pharma & Healthcare": [
        "SUNPHARMA", "CIPLA", "DRREDDY", "DIVISLAB", "LUPIN", "AUROPHARMA",
        "TORNTPHARM", "ZYDUSLIFE", "ALKEM", "GLENMARK", "BIOCON", "IPCALAB",
        "LAURUSLABS", "ABBOTINDIA", "MANKIND", "APOLLOHOSP", "MAXHEALTH",
        "FORTIS", "SYNGENE", "GRANULES",
    ],
    "FMCG": [
        "HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR", "MARICO",
        "GODREJCP", "COLPAL", "TATACONSUM", "UBL", "VBL", "RADICO",
        "EMAMILTD", "JUBLFOOD", "PGHH", "BAJAJCON",
    ],
    "Metals & Mining": [
        "TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL", "JINDALSTEL", "SAIL",
        "NMDC", "NATIONALUM", "HINDZINC", "APLAPOLLO", "JSL", "WELCORP",
        "RATNAMANI", "COALINDIA",
    ],
    "Realty": [
        "DLF", "GODREJPROP", "OBEROIRLTY", "PRESTIGE", "PHOENIXLTD",
        "BRIGADE", "SOBHA", "LODHA", "ANANTRAJ", "SUNTECK", "MAHLIFE",
    ],
    "Oil, Gas & Energy": [
        "RELIANCE", "ONGC", "BPCL", "IOC", "HINDPETRO", "GAIL", "OIL",
        "PETRONET", "IGL", "MGL", "GUJGASLTD", "ATGL", "CASTROLIND",
    ],
    "Power & Utilities": [
        "NTPC", "POWERGRID", "TATAPOWER", "ADANIPOWER", "ADANIENSOL",
        "JSWENERGY", "NHPC", "SJVN", "TORNTPOWER", "CESC", "NLCINDIA",
    ],
    "Financial Services (non-bank)": [
        "BAJFINANCE", "BAJAJFINSV", "JIOFIN", "SHRIRAMFIN", "CHOLAFIN",
        "HDFCLIFE", "SBILIFE", "ICICIPRULI", "ICICIGI", "LICI", "MUTHOOTFIN",
        "MANAPPURAM", "PFC", "RECLTD", "IRFC", "HDFCAMC", "ANGELONE",
        "BSE", "MCX", "CDSL", "POLICYBZR",
    ],
    "Media & Entertainment": [
        "ZEEL", "SUNTV", "PVRINOX", "NAZARA", "SAREGAMA",
        "DBCORP", "HATHWAY", "NETWORK18",
    ],
    "Capital Goods & Infra": [
        "LT", "SIEMENS", "ABB", "BHEL", "BEL", "HAL", "CUMMINSIND", "THERMAX",
        "AIAENG", "KEC", "NBCC", "IRB", "POLYCAB", "HAVELLS", "KEI",
        "SUZLON", "INOXWIND", "CGPOWER", "TRITURBINE", "RVNL",
    ],
    "Cement & Construction": [
        "ULTRACEMCO", "SHREECEM", "AMBUJACEM", "ACC", "DALBHARAT", "JKCEMENT",
        "RAMCOCEM", "INDIACEM", "BIRLACORPN", "JKLAKSHMI",
    ],
    "Chemicals & Fertilisers": [
        "PIDILITIND", "SRF", "UPL", "PIIND", "DEEPAKNTR", "AARTIIND",
        "TATACHEM", "GNFC", "COROMANDEL", "CHAMBLFERT", "NAVINFLUOR",
        "ATUL", "VINATIORGA", "LINDEINDIA", "FLUOROCHEM",
    ],
    "Consumer Durables": [
        "TITAN", "VOLTAS", "CROMPTON", "WHIRLPOOL", "BLUESTARCO", "DIXON",
        "AMBER", "BATAINDIA", "KALYANKJIL", "VGUARD", "RAJESHEXPO",
    ],
    "Telecom": [
        "BHARTIARTL", "IDEA", "INDUSTOWER", "TATACOMM", "HFCL", "TEJASNET",
        "ITI", "STLTECH",
    ],
    "Retail & Consumption": [
        "DMART", "TRENT", "NYKAA", "SWIGGY", "VMART", "SHOPERSTOP",
        "ABFRL", "ETERNAL", "PAYTM", "INDIAMART",
    ],
    "Defence": [
        "HAL", "BEL", "BDL", "MAZDOCK", "COCHINSHIP", "GRSE", "MIDHANI",
        "DATAPATTNS", "ZENTEC", "PARAS", "IDEAFORGE", "ASTRAMICRO",
    ],
    "Textiles": [
        "PAGEIND", "KPRMILL", "TRIDENT", "WELSPUNLIV", "VARDHACRLC",
        "ARVIND", "RAYMOND", "GOKEX", "SUTLEJTEX", "AMBIKCO",
    ],
    "Transport & Logistics": [
        "ADANIPORTS", "CONCOR", "INDIGO", "DELHIVERY", "BLUEDART",
        "TCI", "ALLCARGO", "MAHLOG", "IRCTC", "GESHIP",
    ],
}


def all_symbols():
    """Unique constituent roots across every sector, sorted."""
    seen = set()
    for names in SECTORS.values():
        seen.update(names)
    return sorted(seen)
