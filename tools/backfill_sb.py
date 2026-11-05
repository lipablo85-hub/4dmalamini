"""One-off: Sabah 88 4D history from check4d.org, cross-checked date by date against 4d2ulive.com.
Writes the rows to a separate CSV (never the main one) plus a report; a person merges them.
Dates = Wed/Sat/Sun plus every special draw date Magnum held, same as the other East Malaysia operators."""
import csv, datetime as dt, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

main_csv, out_csv = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(main_csv, encoding="utf-8-sig")))
mdates = {dt.date.fromisoformat(r["date"]) for r in rows if r["operator"] == "Magnum 4D"}
now = dt.datetime.now(F.MYT)
last = now.date() if now.hour * 60 + now.minute >= 1170 else now.date() - dt.timedelta(1)
start = min(mdates)
todo = sorted({d for d in mdates if d <= last} | {start + dt.timedelta(n) for n in range((last - start).days + 1) if (start + dt.timedelta(n)).weekday() in (2, 5, 6)})

def one(url, ref, d):
    for _ in range(3):
        try:
            return F.parse_sb(F.html_text(F.get(url, {"Referer": ref})), d)
        except Exception as e:
            err = e; time.sleep(2)
    print("error", url, err, flush=True)
    return "ERR"

new, miss, conflict, only = [], [], [], []
for d in todo:
    a = one(f"https://www.check4d.org/past-results/{d.isoformat()}", "https://www.check4d.org/", d)
    b = one(f"https://4d2ulive.com/past-results/{d.isoformat()}", "https://4d2ulive.com/", d)
    a = None if a == "ERR" else a; b = None if b == "ERR" else b
    if a and b and (a["top"], a["sp"], a["co"], a["draw_no"]) != (b["top"], b["sp"], b["co"], b["draw_no"]):
        conflict.append(d.isoformat()); print("CONFLICT", d, a, b, flush=True); continue
    r = a or b
    if r:
        new.append(F.row_of(r, d))
        if not (a and b): only.append(f"{d.isoformat()}:{'check4d' if a else '4d2ulive'}")
    else:
        miss.append(d.isoformat())
    time.sleep(0.25)
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=F.COLS); w.writeheader(); w.writerows(new)
print(f"dates tried {len(todo)}; rows {len(new)}; both sources agree on {len(new) - len(only)}; one source only {len(only)} {only[:40]}")
print(f"conflicts {len(conflict)} {conflict}")
print(f"no result on {len(miss)} dates: {miss}")
