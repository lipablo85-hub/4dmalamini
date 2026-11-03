"""Fill specific Singapore 4D draws from singaporepools.com.sg (by draw number)."""
import base64, csv, datetime as dt, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

csv_path, pairs = sys.argv[1], [p.split("=") for p in sys.argv[2:]]   # draw=YYYY-MM-DD
rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
have = {(r["operator"], r["date"]) for r in rows}
new = []
for no, day in pairs:
    if (F.SG, day) in have:
        continue
    q = base64.b64encode(f"DrawNumber={no}".encode()).decode()
    h = F.get(f"https://www.singaporepools.com.sg/en/product/sr/Pages/4d_results.aspx?sppl={q}", {"Referer": "https://www.singaporepools.com.sg/"}).decode("utf-8", "replace")
    g = lambda c: re.findall(r'class="' + c + r'"[^>]*>\s*(\d{4})\s*<', h)
    top = [x for c in ("tdFirstPrize", "tdSecondPrize", "tdThirdPrize") for x in g(c)[:1]]
    def body(c):
        m = re.search(r'<tbody class="' + c + r'">(.*?)</tbody>', h, re.S)
        return re.findall(r">\s*(\d{4})\s*<", m.group(1)) if m else []
    sp, co = body("tbodyStarterPrizes")[:10], body("tbodyConsolationPrizes")[:10]
    ok = F.complete(top, sp, co)
    print(no, day, "OK" if ok else "INCOMPLETE", top, len(sp), len(co))
    if not ok:
        print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))[:600])
        continue
    new.append(F.row_of({"operator": F.SG, "draw_no": no, "top": top, "sp": sp, "co": co}, dt.date.fromisoformat(day)))
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=F.COLS)
    w.writeheader()
    w.writerows(rows + new)
print("added", len(new))
