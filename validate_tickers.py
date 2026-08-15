import urllib.request, urllib.parse, json, concurrent.futures, datetime
from universe import SECTORS, BENCHMARKS, all_symbols
UA={'User-Agent':'Mozilla/5.0'}
def probe(root):
    for suf in ('.NS','.BO'):
        s=root+suf
        try:
            req=urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?range=1mo&interval=1d',headers=UA)
            r=json.load(urllib.request.urlopen(req,timeout=20))['chart']['result'][0]
            cl=r['indicators']['quote'][0]['close']; ts=r['timestamp']
            g=[(t,c) for t,c in zip(ts,cl) if c is not None]
            if len(g)>=8:
                d=datetime.datetime.utcfromtimestamp(g[-1][0]).date()
                if (datetime.date.today()-d).days<=6:
                    return root,s,'OK',str(d),len(g)
                return root,s,'STALE',str(d),len(g)
        except Exception:
            continue
    return root,'','FAIL','',0
roots=all_symbols()
print('universe size:',len(roots))
bad=[]
with concurrent.futures.ThreadPoolExecutor(12) as ex:
    for root,s,st,d,n in ex.map(probe,roots):
        if st!='OK': bad.append((root,st,d,n)); print('  ',root,st,d,n)
print('problem tickers:',len(bad))
