"""One-off: fill Sarawak Cash Sweep history from check4d.org past-results pages.
Dates = Wed/Sat/Sun plus every special draw date Magnum held (Cash Sweep follows the same special draws)."""
import csv, datetime as dt, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

csv_path = sys.argv[1]
rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
have = {(r["operator"], r["date"]) for r in rows}
mdates = {dt.date.fromisoformat(r["date"]) for r in rows if r["operator"] == "Magnum 4D"}
today = dt.datetime.now(F.MYT).date()
start = min(mdates)
todo = sorted({d for d in mdates if d < today} | {start + dt.timedelta(n) for n in range((today - start).days) if (start + dt.timedelta(n)).weekday() in (2, 5, 6)})
new, miss = [], []
for d in todo:
    if (F.CS, d.isoformat()) in have:
        continue
    try:
        r = F.parse_check4d_cs(F.html_text(F.get(f"https://www.check4d.org/past-results/{d.isoformat()}", {"Referer": "https://www.check4d.org/"})), d)
    except Exception as e:
        r = None
        print("error", d, e, flush=True)
    if r:
        new.append(F.row_of(r, d))
    else:
        miss.append(d.isoformat())
    time.sleep(0.3)
with open(csv_path, "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, fieldnames=F.COLS).writerows(new)
print(f"added {len(new)} Cash Sweep draws; no result on {len(miss)} dates: {miss[:60]}")
