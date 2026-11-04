"""One-off: fill GD Lotto 4D history (daily draw) from check4d.org past-results pages.
check4d does not show GD draw numbers on past pages, so those rows are saved without one."""
import csv
import datetime as dt
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

GD = "GD Lotto 4D"


def parse_gd_past(text: str, day: dt.date) -> dict | None:
    m = re.search(r"Grand Dragon 4D.*?Date:\s*(\d{2})-(\d{2})-(\d{4})(.*?)(?:Perdana|Lucky HariHari|Nine|Sandakan|Special CashSweep|\.container)", text, re.S)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    b = m.group(4)
    p = re.search(r"1st\D*?(\d{4}).*?2nd\D*?(\d{4}).*?3rd\D*?(\d{4})", b, re.S)
    sp, co = re.search(r"Special(.*?)Consolation", b, re.S), re.search(r"Consolation(.*)", b, re.S)
    if not (p and sp and co):
        return None
    top = list(p.groups())
    s_ = re.findall(r"\b\d{4}\b", sp.group(1))[:10]
    c_ = re.findall(r"\b\d{4}\b", co.group(1))[:10]
    if F.complete(top, s_, c_):
        return {"operator": GD, "draw_no": "", "top": top, "sp": s_, "co": c_}
    return None


def main() -> int:
    csv_path = sys.argv[1]
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    have = {(r["operator"], r["date"]) for r in rows}
    today = dt.datetime.now(F.MYT).date()
    start = min(dt.date.fromisoformat(r["date"]) for r in rows if r["operator"] == "Magnum 4D")
    new, miss = [], []
    d = start
    while d < today:
        if (GD, d.isoformat()) not in have:
            try:
                r = parse_gd_past(F.html_text(F.get(f"https://www.check4d.org/past-results/{d.isoformat()}", {"Referer": "https://www.check4d.org/"})), d)
            except Exception as e:
                r = None
                print("error", d, e, flush=True)
            if r:
                new.append(F.row_of(r, d))
            else:
                miss.append(d.isoformat())
            if len(new) % 100 == 0 and new:
                print(f"... {len(new)} rows at {d}", flush=True)
            time.sleep(0.25)
        d += dt.timedelta(days=1)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=F.COLS).writerows(new)
    print(f"added {len(new)} GD Lotto draws; no result on {len(miss)} dates: {miss[:40]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
