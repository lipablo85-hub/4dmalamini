"""One-off: fill every missing draw from loto4d.com past-results pages.

Works out which (operator, date) pairs are missing against each operator's own draw schedule,
then fetches one archive page per date and reads whichever operators are still needed from it.
Only complete results (top 3 + 10 Special + 10 Consolation) are saved; anything partial is skipped.
"""
import csv
import datetime as dt
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_results as F

# CSV operator name -> heading on the loto4d page
HEAD = {
    "Magnum 4D": r"Magnum 4D",
    "Sports Toto 4D": r"SportsToto 4D",
    "Da Ma Cai 1+3D": r"Da Ma Cai 1\+3D",
    "GD Lotto 4D": r"Grand Dragon 4D",
    "9 Lotto 4D": r"Nine Lotto",
    "Singapore 4D": r"Singapore 4D",
    "Sarawak Cash Sweep": r"Special CashSweep",
    "Sandakan 4D": r"Sandakan 4D",
}
# headings that may follow a block, used to stop the match
STOP = r"(?:Magnum 4D|SportsToto|Da Ma Cai|Grand Dragon|Nine Lotto|Singapore|SINGAPORE|Special CashSweep|Sandakan|Sabah 88|Lucky HariHari|Perdana|Advertisements|Past 4D|$)"


def parse_op(text: str, op: str, day: dt.date) -> dict | None:
    m = re.search(HEAD[op] + r"[^:]{0,24}Date:\s*(\d{2})-(\d{2})-(\d{4})\s*(?:\([^)]*\))?\s*(?:Draw No:\s*([\w/]+))?(.*?)" + STOP, text, re.S)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    b = m.group(5)
    p = re.search(r"1st\D*?(\d{4}).*?2nd\D*?(\d{4}).*?3rd\D*?(\d{4})", b, re.S)
    sp, co = re.search(r"Special(.*?)Consolation", b, re.S), re.search(r"Consolation(.*)", b, re.S)
    if not (p and sp and co):
        return None
    top = list(p.groups())
    s_ = re.findall(r"\b\d{4}\b", sp.group(1))[:10]
    c_ = re.findall(r"\b\d{4}\b", co.group(1))[:10]
    if F.complete(top, s_, c_):
        return {"operator": op, "draw_no": (m.group(4) or "").strip(), "top": top, "sp": s_, "co": c_}
    return None


def main() -> int:
    csv_path = sys.argv[1]
    since = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else None
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    have = {(r["operator"], r["date"]) for r in rows}
    today = dt.datetime.now(F.MYT).date()
    start = min(dt.date.fromisoformat(r["date"]) for r in rows if r["operator"] == "Magnum 4D")
    days = [start + dt.timedelta(i) for i in range((today - start).days)]
    mag = {r["date"] for r in rows if r["operator"] == "Magnum 4D"}
    wss = [d for d in days if d.weekday() in (2, 5, 6) or d.isoformat() in mag]
    sg = [d for d in days if d.weekday() in (2, 5, 6)]
    sched = {"Magnum 4D": wss, "Sports Toto 4D": wss, "Da Ma Cai 1+3D": wss, "Sarawak Cash Sweep": wss, "Sandakan 4D": wss,
             "Singapore 4D": sg, "GD Lotto 4D": days, "9 Lotto 4D": days}
    need: dict[dt.date, list[str]] = {}
    for op, sc in sched.items():
        for d in sc:
            if since and d < since:
                continue
            if (op, d.isoformat()) not in have:
                need.setdefault(d, []).append(op)
    print(f"{sum(len(v) for v in need.values())} missing results across {len(need)} dates", flush=True)
    new, nf = [], 0
    for i, d in enumerate(sorted(need)):
        pages = []
        for url, ref in (("https://loto4d.com/past-results/" + d.isoformat(), "https://loto4d.com/past-results/"),
                         ("https://www.check4d.org/past-results/" + d.isoformat(), "https://www.check4d.org/")):
            try:
                pages.append(re.sub(r"\s+", " ", F.html_text(F.get(url, {"Referer": ref}))))
            except Exception as e:
                print("fetch error", d, url.split("//")[1][:12], e, flush=True)
        got = []
        for op in need[d]:
            r = None
            for t in pages:
                try:
                    r = parse_op(t, op, d)
                except Exception:
                    r = None
                if r:
                    break
            if r:
                new.append(F.row_of(r, d))
                got.append(op)
            else:
                nf += 1
        if got:
            print(f"{d}: {', '.join(got)}", flush=True)
        if i % 200 == 199:
            print(f"... {i + 1}/{len(need)} dates, {len(new)} rows", flush=True)
        time.sleep(0.25)
    if new:
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=F.COLS).writerows(new)
    print(f"added {len(new)} rows; {nf} not available at source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
