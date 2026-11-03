"""One-off: fill Singapore 4D history (Wed/Sat/Sun draws) from check4d.org past-results pages."""
import csv, datetime as dt, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

csv_path = sys.argv[1]
start = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date(2021, 11, 2)
rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
have = {(r["operator"], r["date"]) for r in rows}
today = dt.datetime.now(F.MYT).date()
new, miss = [], []
d = start
while d < today:
    if d.weekday() in (2, 5, 6) and (F.SG, d.isoformat()) not in have:
        try:
            r = F.parse_check4d_sg(F.html_text(F.get(f"https://www.check4d.org/past-results/{d.isoformat()}", {"Referer": "https://www.check4d.org/"})), d)
        except Exception as e:
            r = None
            print("error", d, e, flush=True)
        if r:
            new.append(F.row_of(r, d))
        else:
            miss.append(d.isoformat())
        time.sleep(0.35)
    d += dt.timedelta(days=1)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=F.COLS)
    w.writeheader()
    w.writerows(rows + new)
print(f"added {len(new)} Singapore 4D draws; no result on {len(miss)} dates: {miss[:40]}")
