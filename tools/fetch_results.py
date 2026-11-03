#!/usr/bin/env python3
"""Fetch tonight's 4D results from the official sites, add them to the CSV and rebuild the site.

Run from cron on your web server every 5 minutes, 7:00-9:00 pm Malaysia time (see README).
Standard library only: no pip install needed.

  python3 tools/fetch_results.py --csv malaysia_4d_draws_2021-2026.csv \
      --build "python3 tools/build.py --results malaysia_4d_draws_2021-2026.csv --dict 4d_dictionary_template.csv --img-src enhanced/ --site https://yourdomain.com/4d/ --out dist.new" \
      --dist dist

Options:
  --date YYYY-MM-DD   draw date to fetch (default: today in Malaysia time)
  --dry-run           show what would be added, change nothing

Behaviour:
  * Only complete results are saved: 1st/2nd/3rd + 10 Special + 10 Consolation, all 4 digits.
    Partial (still drawing) results are skipped and picked up on the next run.
  * A draw already in the CSV is never overwritten. If the site later shows different numbers
    for it, a CONFLICT line is logged so you can check by hand.
  * When something new was added, the site is rebuilt into dist.new and swapped in at once,
    so visitors never see a half-built site.
  * A lock file stops two runs overlapping.
"""
import argparse, csv, datetime as dt, html, json, os, re, shlex, shutil, subprocess, sys, time, urllib.request
from html.parser import HTMLParser
from pathlib import Path

MYT = dt.timezone(dt.timedelta(hours=8))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
COLS = ["operator", "date", "draw_no", "first", "second", "third"] + [f"special_{i}" for i in range(1, 11)] + [f"consolation_{i}" for i in range(1, 11)]


def log(msg: str) -> None:
    print(f"{dt.datetime.now(MYT):%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def get(url: str, headers: dict | None = None, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def d4(x) -> str | None:
    s = str(x).strip()
    return s.zfill(4) if re.fullmatch(r"\d{1,4}", s) else None


def complete(top, sp, co) -> bool:
    return len(top) == 3 and len(sp) == 10 and len(co) == 10 and all(top + sp + co)


# ---------- Magnum 4D: official JSON feed ----------
def parse_magnum(items: list, day: dt.date) -> dict | None:
    for it in items or []:
        if it.get("DrawDate", "") != day.strftime("%d/%m/%Y"):
            continue
        top = [d4(it.get(k, "")) for k in ("FirstPrize", "SecondPrize", "ThirdPrize")]
        sp = [d4(it.get(f"Special{i}", "")) for i in range(1, 11)]
        co = [d4(it.get(f"Console{i}", "")) for i in range(1, 11)]
        sp, co = [x for x in sp if x], [x for x in co if x]
        if complete(top, sp, co):
            return {"operator": "Magnum 4D", "draw_no": it.get("DrawID", "").strip(), "top": top, "sp": sp, "co": co}
    return None


def fetch_magnum(day: dt.date) -> dict | None:
    raw = get(f"https://www.magnum4d.my/results/past/between-dates/null/{day:%Y-%m-%d}/3",
              {"Accept": "application/json", "Referer": "https://www.magnum4d.my/results/draw-results"})
    return parse_magnum(json.loads(raw), day)


# ---------- Da Ma Cai 1+3D: official API -> result file ----------
def parse_damacai(j: dict, day: dt.date) -> dict | None:
    if not j or j.get("drawDate") not in (day.strftime("%d/%m/%Y"), None):
        return None
    top = [d4(j.get(k, "")) for k in ("p1", "p2", "p3")]
    sp = [x for x in (d4(v) for v in j.get("starterList") or []) if x]
    co = [x for x in (d4(v) for v in j.get("consolidateList") or []) if x]
    if complete(top, sp, co):
        return {"operator": "Da Ma Cai 1+3D", "draw_no": str(j.get("drawNo", "")).strip(), "top": top, "sp": sp, "co": co}
    return None


def fetch_damacai(day: dt.date) -> dict | None:
    h = {"cookiesession": "301", "Referer": "https://www.damacai.com.my/"}
    link = json.loads(get(f"https://www.damacai.com.my/callpassresult?pastdate={day:%Y%m%d}", h)).get("link")
    if not link:
        return None
    return parse_damacai(json.loads(get(link)), day)


# ---------- Sports Toto 4D: official past-results page ----------
class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []

    def handle_data(self, d):
        self.out.append(d)

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "tr", "br", "div", "p", "table"):
            self.out.append("\n")


def html_text(b: bytes) -> str:
    p = _Text()
    p.feed(b.decode("utf-8", "replace"))
    return html.unescape(" ".join(p.out))


def parse_toto(text: str, day: dt.date) -> dict | None:
    blocks = re.split(r"(\d+/\d{2}\s*Draw Date\s*:\s*\d+/\d+/\d+)", text)
    for i in range(1, len(blocks) - 1, 2):
        head, body = blocks[i], blocks[i + 1]
        m = re.search(r"(\d+/\d{2})\s*Draw Date\s*:\s*(\d+)/(\d+)/(\d+)", head)
        if not m or dt.date(int(m.group(4)), int(m.group(3)), int(m.group(2))) != day:
            continue
        p = re.search(r"First Prize\s+Second Prize\s+Third Prize\s+(\d{4})\s+(\d{4})\s+(\d{4})", body)
        s = re.search(r"Special Prize\s+(.+?)Consolation Prize", body, re.S)
        c = re.search(r"Consolation Prize\s+(.+?)(?:TOTO 4D JACKPOT|Jackpot|$)", body, re.S)
        if not (p and s and c):
            return None
        top = list(p.groups())
        sp = re.findall(r"\b\d{4}\b", s.group(1))[:10]
        co = re.findall(r"\b\d{4}\b", c.group(1))[:10]
        if complete(top, sp, co):
            return {"operator": "Sports Toto 4D", "draw_no": m.group(1), "top": top, "sp": sp, "co": co}
    return None


def fetch_toto(day: dt.date) -> dict | None:
    raw = get(f"https://www.sportstoto.com.my/results_past.asp?date={day.month}/15/{day.year}",
              {"Referer": "https://www.sportstoto.com.my/"})
    return parse_toto(html_text(raw), day)


# ---------- GD Lotto (Grand Dragon) 4D: official "today" page, daily draw ----------
def parse_gd(text: str, day: dt.date) -> dict | None:
    """Reads the 4D block of gdlotto.net/results/today. Only accepts a complete result for `day`."""
    t = re.sub(r"[ \t\r\f\v]+", " ", text)
    m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", t)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    start = t.find(m.group(0))
    body = t[start:]
    top = []
    for lab in ("1st", "2nd", "3rd"):
        mm = re.search(lab + r"\s*Prize\D{0,40}?(\d{4})\b", body, re.I)
        if not mm:
            return None
        top.append(mm.group(1))
    s_ = re.search(r"Special\b(.*?)Consolation", body, re.S | re.I)
    c_ = re.search(r"Consolation\b(.*?)(?:\b6D\b|6\+1D|Jackpot|Special|Draw\s*No|$)", body[s_.end() - len("Consolation"):] if s_ else "", re.S | re.I)
    if not (s_ and c_):
        return None
    sp = re.findall(r"\b\d{4}\b", s_.group(1))[:10]
    co = re.findall(r"\b\d{4}\b", c_.group(1))[:10]
    no = re.search(r"Draw\s*No\.?\s*:?\s*([\d/]+)", t, re.I)
    if complete(top, sp, co):
        return {"operator": "GD Lotto 4D", "draw_no": no.group(1) if no else "", "top": top, "sp": sp, "co": co}
    return None


def fetch_gd(day: dt.date) -> dict | None:
    raw = get("https://gdlotto.net/results/today/", {"Referer": "https://gdlotto.net/"})
    return parse_gd(html_text(raw), day)


# ---------- 9 Lotto 4D: 9lotto.com/result, daily evening draw ----------
# The page shows only the newest draw and no date, so a result is accepted as `day`'s draw only when
# it is fetched on that day after 7pm MYT AND its draw number is newer than the last 9 Lotto draw saved.
LAST_NO: dict = {}


def _drawkey(no: str):
    m = re.match(r"(\d+)\s*/\s*(\d{4})", no or "")
    return (int(m.group(2)), int(m.group(1))) if m else (0, 0)


def parse_9lotto(text: str) -> dict | None:
    t = re.sub(r"\s+", " ", text)
    no = re.search(r"DRAW\s*NO\.?\s*:?\s*(\d+\s*/\s*\d{4})", t, re.I)
    top = re.search(r"\bI\s*\[?\s*(\d{4})\s*\]?\s*G\s*\[?\s*(\d{4})\s*\]?\s*C\s*\[?\s*(\d{4})\b", t)
    grid = dict(re.findall(r"\b([A-W])\s*:\s*(\d{4}|-{4})", t))
    if not (no and top) or len(grid) < 23:
        return None
    sp = [grid[c] for c in "ABCDEFGHIJKLM" if grid[c].isdigit()]
    co = [grid[c] for c in "NOPQRSTUVW" if grid[c].isdigit()]
    top = list(top.groups())
    if complete(top, sp, co):
        return {"operator": "9 Lotto 4D", "draw_no": re.sub(r"\s", "", no.group(1)), "top": top, "sp": sp, "co": co}
    return None


def fetch_9lotto(day: dt.date) -> dict | None:
    now = dt.datetime.now(MYT)
    if day != now.date() or now.hour < 19:
        return None
    r = parse_9lotto(html_text(get("https://9lotto.com/result", {"Referer": "https://9lotto.com/"})))
    if r and _drawkey(r["draw_no"]) > _drawkey(LAST_NO.get("9 Lotto 4D", "")):
        return r
    return None


FETCHERS = [("Magnum 4D", fetch_magnum), ("Sports Toto 4D", fetch_toto), ("Da Ma Cai 1+3D", fetch_damacai), ("GD Lotto 4D", fetch_gd), ("9 Lotto 4D", fetch_9lotto)]


def row_of(r: dict, day: dt.date) -> dict:
    vals = [r["operator"], day.isoformat(), r["draw_no"]] + r["top"] + r["sp"] + r["co"]
    return dict(zip(COLS, vals))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--build", help="build command; must write to <dist>.new")
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--date")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    day = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(MYT).date()

    lock = Path(a.csv).with_suffix(".lock")
    if lock.exists() and time.time() - lock.stat().st_mtime < 600:
        log("another run is in progress, skipping")
        return 0
    lock.write_text(str(os.getpid()))
    try:
        rows = list(csv.DictReader(open(a.csv, encoding="utf-8-sig")))
        have = {(r["operator"], r["date"]): r for r in rows}
        for r in sorted(rows, key=lambda r: r["date"]):
            LAST_NO[r["operator"]] = r["draw_no"]
        new = []
        for name, fn in FETCHERS:
            if (name, day.isoformat()) in have and not a.dry_run:
                old = have[(name, day.isoformat())]
                try:
                    r = fn(day)
                except Exception:
                    r = None
                if r and [old[c] for c in COLS[3:]] != r["top"] + r["sp"] + r["co"]:
                    log(f"CONFLICT {name} {day}: site now shows different numbers than saved. Check by hand.")
                continue
            try:
                r = fn(day)
            except Exception as e:
                log(f"{name}: could not fetch ({type(e).__name__}: {e})")
                continue
            if not r:
                log(f"{name}: no complete result for {day} yet")
                continue
            new.append(row_of(r, day))
            log(f"{name}: {day} {r['draw_no']} {' '.join(r['top'])}  OK")
        if not new:
            return 0
        if a.dry_run:
            log(f"dry run: would add {len(new)} draw(s)")
            return 0
        tmp = Path(a.csv + ".tmp")
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows + new)
        os.replace(tmp, a.csv)
        log(f"added {len(new)} draw(s) to {a.csv}")
        if a.build:
            subprocess.run(shlex.split(a.build), check=True)
            new_dist, dist, old = Path(a.dist + ".new"), Path(a.dist), Path(a.dist + ".old")
            if not (new_dist / "index.html").exists():
                log("build did not produce " + str(new_dist) + "/index.html; site unchanged")
                return 1
            if old.exists():
                shutil.rmtree(old)
            if dist.exists():
                os.replace(dist, old)
            os.replace(new_dist, dist)
            shutil.rmtree(old, ignore_errors=True)
            log("site rebuilt and published")
        return 0
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
