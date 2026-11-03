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


_C4D: dict = {}


def check4d_text() -> str:
    """check4d.org live page (all companies on one page). Fetched once per run."""
    if "t" not in _C4D:
        _C4D["t"] = html_text(get("https://www.check4d.org/", {"Referer": "https://www.check4d.org/"}))
    return _C4D["t"]


def parse_check4d_toto(text: str, day: dt.date) -> dict | None:
    """Sports Toto 4D block of check4d.org. Blank prize slots show as ****; they are skipped (same as the official page)."""
    m = re.search(r"SportsToto 4D.*?Date:\s*(\d{2})-(\d{2})-(\d{4}).*?Draw No:\s*(\d+/\d{2})(.*?)(?:4D Jackpot 1 Prize|SportsToto 5D)", text, re.S)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    body = m.group(5)
    p = re.search(r"1st\D*?(\d{4}).*?2nd\D*?(\d{4}).*?3rd\D*?(\d{4})", body, re.S)
    sp = re.search(r"Special(.*?)Consolation", body, re.S)
    co = re.search(r"Consolation(.*)$", body, re.S)
    if not (p and sp and co):
        return None
    top = list(p.groups())
    s_ = re.findall(r"\b\d{4}\b", sp.group(1))[:10]
    c_ = re.findall(r"\b\d{4}\b", co.group(1))[:10]
    if complete(top, s_, c_):
        return {"operator": "Sports Toto 4D", "draw_no": m.group(4), "top": top, "sp": s_, "co": c_}
    return None


def _amts(seg: str) -> list:
    """['RM 1,234.50 Won', ...] -> [{'a': '1,234.50', 'w': 'Won'}, ...]"""
    return [{"a": a, **({"w": w} if w else {})} for a, w in re.findall(r"RM\s*([\d,]+(?:\.\d+)?)\s*(Partially Won|Won)?", seg)]


def _block(text: str, start: str, ends: list) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    j = min([k for k in (text.find(e, i + len(start)) for e in ends) if k > 0] or [len(text)])
    return text[i:j]


def parse_check4d_extras(text: str, day: dt.date) -> dict:
    """Jackpots, Toto 5D/6D/lotto, Magnum Life/Gold, blank slots of the Special rows. Only blocks dated `day` are kept."""
    t = re.sub(r"\s+", " ", text)
    want = day.strftime("%d-%m-%Y")
    out: dict = {}

    def dated(b):
        return bool(b) and f"Date: {want}" in b[:200]

    def slots(b):  # Special row as printed, blanks kept as ""
        m = re.search(r"Special\S*\s+(.*?)\s+Consolation", b)
        return [x if x[0].isdigit() else "" for x in re.findall(r"\d{4}|-{4}|\*{4}", m.group(1))] if m else []

    def jp(b):
        m = re.search(r"4D Jackpot 1 Prize 4D Jackpot 2 Prize (.*?)(?:3D Jackpot|Next Draw|$)", b)
        nx = re.search(r"Next Draw Estimated Amount.*?Prize\s+(RM.*?)(?:3D Jackpot|Advertisements|$)", b)
        r = {}
        if m:
            r["jp"] = _amts(m.group(1))[:2]
        if nx:
            r["next"] = [x["a"] for x in _amts(nx.group(1))[:2]]
        return r

    ends4 = ["Advertisements", "Da Ma Cai 1+3D", "SportsToto 4D", "SportsToto 5D", "Da Ma Cai 3+3D", "Magnum Life"]
    b = _block(t, "Magnum 4D 萬能", ends4)
    if dated(b):
        out["M"] = {"sl": slots(b), **jp(b)}
    b = _block(t, "Da Ma Cai 1+3D", ends4)
    if dated(b):
        d = {"sl": slots(b), **jp(b)}
        m3 = re.search(r"3D Jackpot Prize (RM [\d,.]+(?: Partially Won| Won)?)", b)
        if m3:
            d["jp3"] = _amts(m3.group(1))[0]
        out["D"] = d
    b = _block(t, "SportsToto 4D", ["SportsToto 5D", "Advertisements"])
    if dated(b):
        out["T"] = {"sl": slots(b), **jp(b)}
    b = _block(t, "SportsToto 5D", ["Da Ma Cai 3+3D", "Magnum Life", "SINGAPORE", "Advertisements"])
    if dated(b):
        x = out.setdefault("T", {})
        m = re.search(r"5D 1st (\d{5}) 4th (\d{4}) 2nd (\d{5}) 5th (\d{3}) 3rd (\d{5}) 6th (\d{2})", b)
        if m:
            x["d5"] = [m.group(i) for i in (1, 3, 5, 2, 4, 6)]
        m = re.search(r"6D 1st (\d{6})", b)
        if m:
            x["d6"] = m.group(1)
        for key, name in (("star", "Star Toto 6/50"), ("power", "Power Toto 6/55"), ("supreme", "Supreme Toto 6/58")):
            m = re.search(re.escape(name) + r" ((?:\d{1,2} ){6})(?:\+ (\d{1,2}) )?(.*?)(?=Star Toto|Power Toto|Supreme Toto|$)", b)
            if m:
                x[key] = {"n": m.group(1).split(), **({"b": m.group(2)} if m.group(2) else {}), "jp": _amts(m.group(3))[:2]}
    b = _block(t, "Da Ma Cai 3+3D", ["Magnum Life", "Magnum Jackpot Gold", "SINGAPORE", "Advertisements"])
    if dated(b):
        rows = re.findall(r"(\d{6}) ([A-Z]+) Bonus (\d) (RM [\d,.]+(?: Partially Won| Won)?)", b)
        if len(rows) == 3:
            out.setdefault("D", {})["b33"] = [{"n": n, "z": z.title(), **_amts(a)[0]} for n, z, _, a in rows]
    b = _block(t, "Magnum Life", ["Magnum Jackpot Gold", "SINGAPORE", "Advertisements"])
    if dated(b):
        m = re.search(r"Winning Numbers ((?:\d{2} ){8})Bonus Numbers (\d{2}) (\d{2})", b)
        if m:
            out.setdefault("M", {})["life"] = {"n": m.group(1).split(), "b": [m.group(2), m.group(3)]}
    b = _block(t, "Magnum Jackpot Gold", ["SINGAPORE", "Advertisements"])
    if dated(b):
        m = re.search(r"Jackpot 1 ((?:\d ){6})\+ ((?:\d ){2})Prize : (RM [\d,.]+(?: Partially Won| Won)?).*?Jackpot 2 .*?Prize : (RM [\d,.]+(?: Partially Won| Won)?)", b)
        if m:
            out.setdefault("M", {})["gold"] = {"n": m.group(1).replace(" ", ""), "b": m.group(2).replace(" ", ""), "jp": _amts(m.group(3)) + _amts(m.group(4))}
    if out:
        out["date"] = day.isoformat()
    return out


def fetch_toto(day: dt.date) -> dict | None:
    """Official page first; it blocks most cloud servers (GitHub included), so fall back to check4d.org."""
    try:
        raw = get(f"https://www.sportstoto.com.my/results_past.asp?date={day.month}/15/{day.year}",
                  {"Referer": "https://www.sportstoto.com.my/"})
        r = parse_toto(html_text(raw), day)
        if r:
            return r
    except Exception as e:
        log(f"Sports Toto official page unavailable ({type(e).__name__}); using check4d.org")
    return parse_check4d_toto(check4d_text(), day)


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


def parse_check4d_gd(text: str, day: dt.date) -> dict | None:
    """Grand Dragon block of check4d.org (no draw number shown: continue our own GD numbering)."""
    m = re.search(r"Grand Dragon 4D.*?Date:\s*(\d{2})-(\d{2})-(\d{4})(.*?)(?:Perdana|Lucky HariHari|\.container)", text, re.S)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    body = m.group(4)
    p = re.search(r"1st\D*?(\d{4}).*?2nd\D*?(\d{4}).*?3rd\D*?(\d{4})", body, re.S)
    sp = re.search(r"Special(.*?)Consolation", body, re.S)
    co = re.search(r"Consolation(.*)$", body, re.S)
    last = LAST_NO.get("GD Lotto 4D", "")
    n = re.match(r"(\d+)/", last)
    if not (p and sp and co and n):
        return None
    top, s_, c_ = list(p.groups()), re.findall(r"\b\d{4}\b", sp.group(1))[:10], re.findall(r"\b\d{4}\b", co.group(1))[:10]
    if complete(top, s_, c_):
        return {"operator": "GD Lotto 4D", "draw_no": f"{int(n.group(1)) + 1}/{day.year}", "top": top, "sp": s_, "co": c_}
    return None


def fetch_gd(day: dt.date) -> dict | None:
    try:
        r = parse_gd(html_text(get("https://gdlotto.net/results/today/", {"Referer": "https://gdlotto.net/"})), day)
        if r:
            return r
    except Exception as e:
        log(f"GD Lotto official page unavailable ({type(e).__name__}); using check4d.org")
    return parse_check4d_gd(check4d_text(), day)


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
    # top three follow the draw number, each after a letter that changes per draw (e.g. "M 8079 K 4362 I 0424")
    top = re.search(r"DRAW\s*NO\.?\s*:?\s*\d+\s*/\s*\d{4}\s+[A-W]\s*\[?\s*(\d{4})\s*\]?\s+[A-W]\s*\[?\s*(\d{4})\s*\]?\s+[A-W]\s*\[?\s*(\d{4})\b", t, re.I)
    grid = dict(re.findall(r"\b([A-W])\s*:\s*(\d{4}|-{4})", t))
    if not (no and top) or len(grid) < 23:
        return None
    sp = [grid[c] for c in "ABCDEFGHIJKLM" if grid[c].isdigit()]
    co = [grid[c] for c in "NOPQRSTUVW" if grid[c].isdigit()]
    top = list(top.groups())
    if complete(top, sp, co):
        return {"operator": "9 Lotto 4D", "draw_no": re.sub(r"\s", "", no.group(1)), "top": top, "sp": sp, "co": co}
    return None


N7, N9 = "9 Lotto 4D", "9 Lotto 4D 9PM"   # one draw a day at 7pm (N9: old label, no longer used)
HIST9: list = []   # [(date, slot 7|9, (year, number))] of saved 9 Lotto draws, oldest first; filled by main()
_PAGE9: dict = {}


def _slot9(key, now) -> int | None:
    """Which slot (7 or 9) a newly seen 9 Lotto draw belongs to, tonight.
    Draw numbers go up by one per draw (7pm, 9pm, next day 7pm ...), so we count on from the last saved draw.
    If that chain is broken (missed days, new year), fall back to the clock: before 9pm = 7pm draw."""
    if HIST9:
        d, slot, last = HIST9[-1]
        if key <= last:
            return None
        if key[0] == last[0]:
            for _ in range(key[1] - last[1]):
                d, slot = (d, 9) if slot == 7 else (d + dt.timedelta(days=1), 7)
            if d == now.date():
                return slot
            if d < now.date() - dt.timedelta(days=0):
                pass  # chain says an older draw: we missed some, use the clock
            else:
                return None
    return 7 if now.hour < 21 else 9


def parse_loto4d_9(text: str, day: dt.date) -> dict | None:
    """Nine Lotto block of loto4d.com (newest 9 Lotto draw, any slot)."""
    t = re.sub(r"\s+", " ", text)
    m = re.search(r"Nine Lotto Date:\s*(\d{2})-(\d{2})-(\d{4}).*?Draw No:\s*(\d+/\d{4})(.*?)(?:Magnum 4D|SportsToto|Da Ma Cai|Grand Dragon|Perdana|$)", t)
    if not m or dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) != day:
        return None
    b = m.group(5)
    p = re.search(r"1st Prize \S+ (\d{4}) 2nd Prize \S+ (\d{4}) 3rd Prize \S+ (\d{4})", b)
    sp = re.search(r"Special(.*?)Consolation", b)
    co = re.search(r"Consolation(.*)$", b)
    if not (p and sp and co):
        return None
    top, s_, c_ = list(p.groups()), re.findall(r"\b\d{4}\b", sp.group(1))[:10], re.findall(r"\b\d{4}\b", co.group(1))[:10]
    if complete(top, s_, c_):
        return {"operator": "9 Lotto 4D", "draw_no": m.group(4), "top": top, "sp": s_, "co": c_}
    return None


def _fetch9(day: dt.date, want: int) -> dict | None:
    now = dt.datetime.now(MYT)
    if day != now.date() or now.hour < 19:   # 9 Lotto draws once a day at 7pm
        return None
    if "r" not in _PAGE9:
        try:
            _PAGE9["r"] = parse_9lotto(html_text(get("https://9lotto.com/result", {"Referer": "https://9lotto.com/"})))
        except Exception as e:
            log(f"9 Lotto official page unavailable ({type(e).__name__})")
            _PAGE9["r"] = None
        if not _PAGE9["r"]:
            try:
                _PAGE9["r"] = parse_loto4d_9(html_text(get("https://loto4d.com/", {"Referer": "https://loto4d.com/"})), now.date())
                if _PAGE9["r"]:
                    log("9 Lotto: using loto4d.com")
            except Exception as e:
                log(f"9 Lotto loto4d unavailable ({type(e).__name__})")
    r = _PAGE9["r"]
    if not r:
        return None
    last = HIST9[-1][2] if HIST9 else (0, 0)
    if _drawkey(r["draw_no"]) <= last:   # still showing a draw we already have
        return None
    return dict(r, operator=N7)


def fetch_9lotto_7pm(day: dt.date) -> dict | None:
    return _fetch9(day, 7)


# ---------- Super J3 & J9: superj3.net JSON feed, two sessions a day (3pm = "J3", 9pm = "J9") ----------
J3, J9 = "Super J3 3PM", "Super J9 9PM"
J3KEY = "e0a5d3fsdfdsghhg18b0c8bgfdgd7c06e"   # public key embedded in superj3.net's own page
_J3: dict = {}


def j3_landing() -> dict:
    if "j" not in _J3:
        _J3["j"] = json.loads(get(f"https://superj3.net/data/data-api.php?op=get_landing_info&api_key={J3KEY}&ao=1", {"Referer": "https://superj3.net/"}))
    return _J3["j"]


def parse_j3(r: dict) -> dict | None:
    """One superj3.net draw -> our row; SP A-M (blanks "-"), CS N-W."""
    top = [d4(r.get(k, "")) for k in ("FIRST", "SECOND", "THIRD")]
    sp = [d4(v) for v in (r.get("SP") or {}).values()]
    co = [d4(v) for v in (r.get("CS") or {}).values()]
    sp, co = [x for x in sp if x], [x for x in co if x]
    if not complete(top, sp, co):
        return None
    return {"top": top, "sp": sp, "co": co, "draw_no": ""}


def _fetch_j(day: dt.date, dtk: str, name: str) -> dict | None:
    now = dt.datetime.now(MYT)
    if day == now.date() and now.hour < int(dtk):
        return None
    j = j3_landing()
    r = (j.get("last_result") or {}).get(f"{day:%Y%m%d}_{dtk}")
    if not r:
        want = ("3PM" if dtk == "15" else "9PM")
        r = next((x for x in j.get("past_results") or [] if x.get("DATE", "")[:10] == day.isoformat() and x.get("TIME") == want), None)
    p = parse_j3(r) if r else None
    return dict(p, operator=name) if p else None


def fetch_j3(day: dt.date) -> dict | None:
    return _fetch_j(day, "15", J3)


def fetch_j9(day: dt.date) -> dict | None:
    return _fetch_j(day, "21", J9)


FETCHERS = [("Magnum 4D", fetch_magnum), ("Sports Toto 4D", fetch_toto), ("Da Ma Cai 1+3D", fetch_damacai), ("GD Lotto 4D", fetch_gd), (N7, fetch_9lotto_7pm), (J3, fetch_j3), (J9, fetch_j9)]


def save_extras(path: Path, day: dt.date, dry: bool) -> None:
    """Merge tonight's jackpots / 5D / 6D / lotto / blank slots into extras.json (keyed YYYYMMDD, last 40 draw days)."""
    try:
        x = parse_check4d_extras(check4d_text(), day)
    except Exception as e:
        log(f"extras: could not fetch ({type(e).__name__}: {e})")
        return
    x.pop("date", None)
    if not x:
        log(f"extras: nothing for {day} yet")
        return
    j = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    key = day.strftime("%Y%m%d")
    cur = j.get(key, {})
    for k, v in x.items():
        cur[k] = {**cur.get(k, {}), **v}
    if j.get(key) == cur:
        return
    j[key] = cur
    j = {d: j[d] for d in sorted(j)[-40:]}
    log(f"extras: {key} " + ", ".join(f"{k}:{'/'.join(sorted(v))}" for k, v in cur.items()))
    if not dry:
        path.write_text(json.dumps(j, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


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
    ap.add_argument("--pending", action="store_true", help="print the draws due today that are not saved yet, then exit")
    a = ap.parse_args()
    day = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(MYT).date()
    if a.pending:
        rows = list(csv.DictReader(open(a.csv, encoding="utf-8-sig")))
        have = {(r["operator"], r["date"]) for r in rows}
        now = dt.datetime.now(MYT)
        mins = (now.hour * 60 + now.minute) if day == now.date() else 24 * 60
        due = ([J3] if mins >= 900 else []) + (["GD Lotto 4D", N7] if mins >= 1140 else []) + (["Magnum 4D", "Sports Toto 4D", "Da Ma Cai 1+3D"] if day.weekday() in (2, 5, 6) and mins >= 1140 else []) + ([J9] if mins >= 1260 else [])
        for name in due:
            if (name, day.isoformat()) not in have:
                print(name)
        xf = Path(a.csv).with_name("extras.json")
        if day.weekday() in (2, 5, 6):
            x = json.loads(xf.read_text(encoding="utf-8")).get(day.strftime("%Y%m%d"), {}) if xf.exists() else {}
            if not (x.get("T", {}).get("d6") and x.get("M", {}).get("jp") and x.get("D", {}).get("b33")):
                print("extras")
        return 0

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
        for r in sorted((r for r in rows if r["operator"] in (N7, N9)), key=lambda r: (r["date"], r["operator"] == N9)):
            HIST9.append((dt.date.fromisoformat(r["date"]), 9 if r["operator"] == N9 else 7, _drawkey(r["draw_no"])))
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
        save_extras(Path(a.csv).with_name("extras.json"), day, a.dry_run)
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
