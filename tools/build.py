#!/usr/bin/env python3
"""Build the 4D Result History site into a fast, upload-ready folder.

Usage:
  python3 build.py --results malaysia_4d_draws.csv [--dict 4d_dictionary.csv] [--img-src pictures/] [--text dict_text/] \
                   [--site https://yourdomain.com/4d/] [--template page.template.html] [--out dist]

What it does:
  * results CSV  -> data/results.<hash>.json   (compact; cached forever, renamed when it changes)
  * dictionary CSV (rows with any meaning filled) -> data/dict.<hash>.txt (loaded only when the Dictionary tab opens)
  * page template -> index.html with English text pre-filled (shows on first paint), minified if
    html-minifier-terser is installed (npm i -g html-minifier-terser)
  * sw.js (offline + instant repeat visits), manifest.webmanifest, icons, _headers and .htaccess cache rules

Run it again after every draw (add the new rows to the results CSV) and upload the dist folder.
"""
import argparse, csv, hashlib, html as H, json, re, shutil, subprocess
from pathlib import Path

OPS = {"Magnum 4D": "M", "Sports Toto 4D": "T", "Da Ma Cai 1+3D": "D", "GD Lotto 4D": "G", "9 Lotto 4D": "N", "9 Lotto 4D 9PM": "N", "Super J3 3PM": "J", "Super J9 9PM": "K", "Singapore 4D": "S", "Sarawak Cash Sweep": "C", "Sabah 88 4D": "B", "Sandakan 4D": "H"}


def h8(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:8]


def build_results(path: Path) -> bytes:
    rows = {k: [] for k in OPS.values()}
    seen = set()
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        k = OPS.get(r["operator"].strip())
        if not k:
            raise SystemExit(f"Unknown operator: {r['operator']!r} (expected one of {list(OPS)})")
        d = r["date"].replace("-", "")
        nums = [r["first"], r["second"], r["third"]] + [r[f"special_{i}"] for i in range(1, 11)] + [r[f"consolation_{i}"] for i in range(1, 11)]
        nums = [n.strip().zfill(4) for n in nums]
        if not re.fullmatch(r"\d{8}", d) or not all(re.fullmatch(r"\d{4}", n) for n in nums):
            raise SystemExit(f"Bad row: {r['operator']} {r['date']} {nums}")
        if (k, d) in seen:
            raise SystemExit(f"Duplicate draw: {r['operator']} {r['date']}")
        seen.add((k, d))
        rows[k].append(f"{d},{r['draw_no'].strip()},{''.join(nums)}")
    data = {k: "|".join(sorted(v)) for k, v in rows.items() if v}
    print("  results:", {k: len(v) for k, v in rows.items()})
    return json.dumps(data, separators=(",", ":")).encode()


def build_dict(path: Path | None, imgs: set, text: dict | None = None) -> list:
    out, done = [], set()
    text = text or {}
    for r in (csv.DictReader(open(path, encoding="utf-8-sig")) if path else []):
        n = r["number"].strip().zfill(4)
        vals = [r.get("category", ""), r.get("chinese_中文", ""), r.get("english", ""), r.get("malay_bahasa_melayu", ""), r.get("tamil_தமிழ்", "")]
        vals = [v.replace("|", "/").replace("\n", " ").strip() for v in vals]
        img = "1" if n in imgs else ""
        if n in text and not any(vals[1:]):
            vals = [vals[0]] + text[n]
        if any(vals[1:]) or img:
            out.append("|".join([n] + vals + [img]))
            done.add(n)
    for n in sorted((imgs | set(text)) - done):
        t = text.get(n, ["", "", "", ""])
        out.append("|".join([n, ""] + t + ["1" if n in imgs else ""]))
    out.sort()
    print(f"  dictionary entries: {len(out)} ({len(imgs)} with pictures)")
    return out


def load_text(folder: Path) -> dict:
    """Read NNNN.tsv files: number, chinese, english, malay, tamil, flag."""
    text = {}
    for f in sorted(folder.glob("*.tsv")):
        for line in f.read_text(encoding="utf-8").splitlines():
            a = (line.split("\t") + [""] * 6)[:6]
            if re.fullmatch(r"\d{4}", a[0]) and a[5] != "missing" and any(a[1:5]):
                text[a[0]] = [x.replace("|", "/").strip() for x in a[1:5]]
    print(f"  dictionary text: {len(text)} entries from {folder}")
    return text


def lang_strings(html: str, lang: str) -> dict:
    m = re.search(r"\n" + lang + r":\{(.*?)\}(?:,\s*\n(?:en|ms|zh|ta):\{|\s*\n\};)", html, re.S)
    return dict(re.findall(r'(\w+):"((?:[^"\\]|\\.)*)"', m.group(1)))


def prerender_lang(html: str, lang: str) -> str:
    t, en = lang_strings(html, lang), lang_strings(html, "en")
    return re.sub(r'data-t="(\w+)"([^>]*)></', lambda x: f'data-t="{x.group(1)}"{x.group(2)}>{H.escape(t.get(x.group(1)) or en.get(x.group(1), ""), quote=False)}</', html)


def board_lang(html: str, lang: str) -> str:
    """Prize labels and jackpot captions in the page's language, written as the script writes them, so
    the card layout (Malay and Tamil labels wrap) is final at first paint."""
    if lang == "en": return html
    t = lang_strings(html, lang)
    zh = {"p1": "首奖", "p2": "二奖", "p3": "三奖", "p4": "特别奖", "p5": "安慰奖"}
    en = {"p1": "1st Prize", "p2": "2nd Prize", "p3": "3rd Prize", "p4": "Special", "p5": "Consolation"}
    lab = lambda k: H.escape(t.get(k, en[k]), quote=False) if lang == "zh" else f'{H.escape(t.get(k, en[k]), quote=False)}<em>{zh[k]}</em>'
    for k in ("p1", "p2", "p3"):
        html = html.replace(f"<span>{en[k]}<em>{zh[k]}</em></span>", f"<span>{lab(k)}</span>")
    for k in ("p4", "p5"):
        html = html.replace(f'<div class="sec">{en[k]}<em>{zh[k]}</em></div>', f'<div class="sec">{lab(k)}</div>')
    g = lambda k, d: H.escape(t.get(k, d), quote=False)
    html = html.replace("<span>★ 4D Jackpot</span>", f"<span>★ {g('jpBar', '4D Jackpot')}</span>")
    html = re.sub(r"<small>Jackpot (\d)</small>", lambda m: f"<small>{g('jpN', 'Jackpot {n}').replace('{n}', m.group(1))}</small>", html)
    html = html.replace("<small>3D Jackpot</small>", f"<small>{g('jp3', '3D Jackpot')}</small>").replace("<small>6D Jackpot</small>", f"<small>{g('j6', '6D Jackpot')}</small>")
    html = html.replace('<div class="nx">Next draw estimate:', f'<div class="nx">{g("nextEst", "Next draw estimate")}:')
    html = re.sub(r'(class="rsb" data-rs="[^"]+") aria-label="Share"', lambda m: f'{m.group(1)} aria-label="{H.escape(t.get("shareBtn", "Share"))}"', html)
    return html


def rd_label(html: str, lang: str) -> str:
    """The date button label in the page's own language, formatted by Intl exactly as the script does
    (node has the same ICU data), so the label doesn't change length - or wrap - when the script runs."""
    m = re.search(r'<span id="rdlabel">Latest · ([^<]*)</span>', html)
    if not m: return html
    d = _RD.get("d")
    if not d: return html
    tag = lang_strings(html, lang).get("latestTag", "Latest")
    if lang not in _RD:
        import subprocess
        loc = {"en": "en-MY", "ms": "ms-MY", "zh": "zh-CN", "ta": "ta-MY"}[lang]
        js = (f'console.log(new Intl.DateTimeFormat("{loc}",{{timeZone:"UTC",weekday:"short",day:"numeric",month:"short",year:"numeric"}})'
              f'.format(Date.UTC({int(d[:4])},{int(d[4:6]) - 1},{int(d[6:])})))')
        try:
            _RD[lang] = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            _RD[lang] = ""
    if not _RD[lang]: return html
    return html.replace(m.group(0), f'<span id="rdlabel">{H.escape(tag)} · {H.escape(_RD[lang])}</span>')


_RD: dict = {}


def prerender_spd(html: str) -> str:
    """The special-draw pill as the script draws it (English; the script relabels it), so it doesn't pop in."""
    import datetime
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    ymd, m = now.strftime("%Y%m%d"), now.hour * 60 + now.minute
    dates = [d.replace("-", "") for d in json.loads(Path(__file__).with_name("special_draws.json").read_text())["dates"]]
    nx = next((d for d in dates if d > ymd or (d == ymd and m < 1140 + 90)), None)
    tag = '<a class="spd" id="spd" href="special-draw/" hidden></a>'
    if not nx or tag not in html: return html
    dd = (datetime.date(int(nx[:4]), int(nx[4:6]), int(nx[6:])) - now.date()).days
    day = datetime.date(int(nx[:4]), int(nx[4:6]), int(nx[6:]))
    cd = "Today" if dd == 0 else "Tomorrow" if dd == 1 else f"in {dd} days"
    pill = (f'<a class="spd{" today" if dd == 0 else ""}" id="spd" href="special-draw/" title="Magnum, Sports Toto, Da Ma Cai, Cash Sweep, Sabah 88, Sandakan">'
            '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'
            f'<b>Special draw</b><span>{day.day} {day.strftime("%b")} ({day.strftime("%a")}) · 7:00pm</span><span class="cd">· {cd}</span></a>')
    return html.replace(tag, pill)


def jp_bar(x) -> str:
    """Same markup as jpBar() in the page script, so the first script render keeps the card height."""
    if not x or not x.get("jp"): return ""
    w = lambda j: "" if not j or not j.get("w") else f'<span class="w {"f" if j["w"] == "Won" else "p"}">{"Won" if j["w"] == "Won" else "Partially won"}</span>'
    out = ('<div class="jp"><div class="jh"><span>★ 4D Jackpot</span><span>积宝</span></div><div class="jr">'
           + "".join(f'<div><small>Jackpot {i + 1}</small><strong>RM {j["a"]}</strong>{w(j)}</div>' for i, j in enumerate(x["jp"])) + "</div>")
    if x.get("jp3"): out += f'<div class="j3"><small>3D Jackpot</small><strong>RM {x["jp3"]["a"]}</strong></div>'
    if x.get("next") and len(x["next"]) == 2: out += f'<div class="nx">Next draw estimate: <b>RM {x["next"][0]}</b> · <b>RM {x["next"][1]}</b></div>'
    return out + "</div>"


def j6(k: str, t3: list) -> str:
    if k not in "JK": return ""
    v = "".join(x[2:] for x in t3) if all(re.fullmatch(r"\d{4}", x or "") for x in t3) else ""
    return f'<div class="j6d"><small>6D Jackpot</small><b>{v}</b></div>' if v else '<div class="j6d wait"><small>6D Jackpot</small><b>------</b></div>'


def prerender_latest(html: str, data: dict, xt: dict | None = None) -> str:
    """Write the results board (classic result slips, official draw order) into the page; the page script redraws it in the visitor's language."""
    import datetime
    board = [("M", "Magnum 4D", "#E9C46B"), ("D", "Da Ma Cai", "#4C8DFF"), ("T", "Sports Toto", "#FF5A5F"), ("S", "Singapore 4D", "#38BDF8"), ("C", "Cash Sweep", "#4ADE80"), ("B", "Sabah 88", "#E5484D"), ("H", "Sandakan 4D", "#FACC15"), ("G", "GD Lotto", "#F27BA5"), ("N", "9 Lotto", "#2EC4B6"), ("J", "Super J3 3pm", "#A78BFA"), ("K", "Super J9 9pm", "#FB923C")]
    zh = {"M": "万能", "D": "大马彩", "T": "多多", "G": "豪龙", "N": "", "J": "J3 下午3点", "K": "J9 晚上9点", "S": "新加坡万字", "C": "砂拉越大万", "B": "沙巴88", "H": "山打根"}
    hc = {"M": "#FFF200", "D": "#000080", "T": "#C00000", "G": "#B0121B", "N": "#0E8F86", "J": "#5B21B6", "K": "#C2410C", "S": "#B91C2C", "C": "#0B7A3B", "B": "#D7141A", "H": "#14532D"}
    fd = lambda d: datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("%a, %-d %b %Y")
    cdf = lambda d: datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("(%a) %d-%b-%Y")
    nb = lambda n: f'<button type="button" data-n="{n}">{n}</button>'
    head = lambda k, name, sub, rs="": (f'<div class="sh"><span class="lgw">{('<img class="opl" src="img/op/n-s.webp" width="46" height="46" alt="9 Lotto">' if k == "N" else f'<img class="opl" src="img/op/{k.lower()}{"-n" if k in "DT" else ""}.webp?v=4" width="40" height="40" alt="">')}</span>'
                                 f'<div class="sht"><b>{name} {f"<i>{zh[k]}</i>" if zh[k] else ""}</b><small>{sub}</small></div>{rs}</div>')
    lb = '<div class="lbar"><span>1st Prize<em>首奖</em></span><span>2nd Prize<em>二奖</em></span><span>3rd Prize<em>三奖</em></span></div>'
    cards, last = [], ""
    for k, name, c in board:
        stl = f'style="--c:{c};--hb:{hc[k]}"'
        if k not in data:
            cards.append(f'<article class="rc slip soon k-{k}" id="rc-{k}" {stl}>{head(k, name, "Soon")}<div class="rb">Results coming soon</div></article>')
            continue
        d, no, dg = data[k].split("|")[-1].split(",")
        last = max(last, d)
        n = [dg[i:i + 4] for i in range(0, 92, 4)]
        rsb = (f'<button type="button" class="rsb" data-rs="{k}|{d}" aria-label="Share"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">'
               '<circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"></path></svg></button>')
        cards.append(f'<article class="rc slip k-{k}" id="rc-{k}" {stl}>{head(k, name, cdf(d) + (f" #{no}" if no else ""), rsb)}{lb}'
                     f'<div class="s3">{"".join(nb(x) for x in n[:3])}</div>'
                     f'<div class="sec">Special<em>特别奖</em></div><div class="s5">{"".join(nb(x) for x in sorted(n[3:13]))}</div>'
                     f'<div class="sec">Consolation<em>安慰奖</em></div><div class="s5">{"".join(nb(x) for x in sorted(n[13:]))}</div>'
                     f'{jp_bar((xt or {}).get(d, {}).get(k))}{j6(k, n[:3])}</article>')
    # DOM order = the order the page shows at build time (same rules as the .nd/.sJ/.sK CSS), so a
    # half-loaded board doesn't paint Magnum first and then jump when the daily games arrive.
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    sp = [x.replace("-", "") for x in json.loads(Path(__file__).with_name("special_draws.json").read_text())["dates"]]
    nd = now.weekday() not in (2, 5, 6) and now.strftime("%Y%m%d") not in sp
    mm = now.hour * 60 + now.minute
    rank = {"G": -3, "N": -2, "J": -1, "K": -1} if nd else {}
    if nd and 895 <= mm < 1135: rank["J"] = -9
    elif nd and mm >= 1255: rank["K"] = -9
    order = sorted(range(len(board)), key=lambda i: (rank.get(board[i][0], 0), i))
    cards = [cards[i] for i in order]
    jump = "".join(f'<a href="#rc-{k}" style="--c:{c}"><i></i>{name}</a>' for k, name, c in board)
    assert "<!--BOARD-->" in html
    html = html.replace("<!--BOARD-->", "".join(cards)).replace('<nav class="jump" id="rjump" aria-label="Jump to company"></nav>', f'<nav class="jump" id="rjump" aria-label="Jump to company">{jump}</nav>')
    _RD["d"] = last
    return html.replace('<span id="rdlabel"></span>', f'<span id="rdlabel">Latest · {fd(last)}</span>')


def prerender_static(html: str, data: dict) -> str:
    """Write the first-screen parts (company buttons, date range, most-frequent numbers) into the page,
    so nothing moves when the results data arrives (no layout shift)."""
    import datetime, collections, re as _re
    m = _re.search(r"const OPS=\[(.*?)\];", html, _re.S)
    ops = _re.findall(r'\{(?:k:"(\w)",)?name:"([^"]+)",zh:"[^"]*",c:"(#[0-9A-Fa-f]{6})"\}', m.group(1))
    btn = []
    for k, name, c in ops:
        if k:
            btn.append(f'<button type="button" class="op" data-op="{k}" aria-pressed="true" style="background:{c};border-color:{c}"><i style="background:{c}"></i>{name}</button>')
        else:
            btn.append(f'<button type="button" class="op" disabled><i style="background:{c}"></i>{name}<small>Soon</small></button>')
    html = html.replace('<div class="ops" id="ops" role="group" hidden></div>', '<div class="ops" id="ops" role="group" aria-label="By operator" hidden>' + "".join(btn) + "</div>")
    rows = [r.split(",") for v in data.values() for r in v.split("|")]
    dates = sorted({r[0] for r in rows})
    d0, d1 = (datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])) for d in (dates[0], dates[-1]))
    rng = f"{d0:%b %Y} – {d1.day} {d1:%b %Y} · {len(rows):,} draws"
    html = html.replace('<p class="sub" id="range"></p>', f'<p class="sub" id="range">{rng}</p>').replace('<p class="sub" id="range2"></p>', f'<p class="sub" id="range2">{rng}</p>')
    c = collections.Counter(r[2][i:i + 4] for r in rows for i in range(0, 92, 4))
    top = sorted(c.items(), key=lambda x: (-x[1], x[0]))[:12]
    chips = "".join(f'<button type="button" class="chip" data-n="{n}"><span class="mono">{n}</span><span>{k} times</span></button>' for n, k in top)
    html = html.replace('<div class="freq" id="freq"></div>', f'<div class="freq" id="freq">{chips}</div>')
    for i, d in (("df", d0), ("dto", d1)):
        html = html.replace(f'<input type="date" id="{i}">', f'<input type="date" id="{i}" value="{d.isoformat()}" min="{d0.isoformat()}" max="{d1.isoformat()}">')
    return html


def external_app(html: str, out: Path) -> str:
    """Move the app script (~100 KB, identical in all four languages) into a fingerprinted file.

    It is cached forever (/assets/* is immutable, and the service worker serves it cache-first),
    so repeat visits and language switches only download the HTML. The tag goes in <head> with
    defer: it downloads in parallel with the page and still runs after parsing, as before."""
    blocks = [m for m in re.finditer(r"<script>(.*?)</script>", html, re.S)]
    m = max(blocks, key=lambda x: len(x.group(1)))
    js = m.group(1).encode()
    if len(js) < 20000: return html
    name = f"assets/app.{h8(js)}.js"
    (out / name).parent.mkdir(parents=True, exist_ok=True); (out / name).write_bytes(js)
    html = html[:m.start()] + html[m.end():]
    return html.replace("</head>", f'<script src="/{name}" defer></script></head>', 1)


def icons(out: Path) -> None:
    """Copy the 4D Malam Ini brand files (favicon, app icons, share image) into the site root."""
    brand = Path(__file__).with_name("brand")
    for f in ("favicon.svg", "favicon-32.png", "favicon-96.png", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "og-image.jpg"):
        if (brand / f).exists():
            shutil.copy2(brand / f, out / f)
        else:
            print(f"  ! brand file missing: tools/brand/{f}")
    if (brand / "op").is_dir():
        shutil.copytree(brand / "op", out / "img" / "op", dirs_exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--dict")
    ap.add_argument("--img-src", help="folder of dictionary pictures from wzt_img.py")
    ap.add_argument("--text", help="folder of NNNN.tsv dictionary text (chinese/english/malay/tamil)")
    ap.add_argument("--site", default="https://yourdomain.com/")
    ap.add_argument("--template", default=str(Path(__file__).with_name("page.template.html")))
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)

    res = build_results(Path(a.results))
    res_name = f"data/results.{h8(res)}.json"
    (out / res_name).write_bytes(res)

    imgs = set()
    if a.img_src and (Path(a.img_src) / "240").is_dir():
        # sprite sheets from tools/sprite_img.py: 25 pictures per file
        shutil.copytree(a.img_src, out / "img" / "d2")
        for p in (Path(a.img_src) / "240").glob("*.avif"):
            sh = int(p.stem)
            imgs.update(f"{n:04d}" for n in range(sh * 25, sh * 25 + 25))
    elif a.img_src:
        dst = out / "img" / "dict"
        dst.mkdir(parents=True)
        for p in Path(a.img_src).iterdir():
            m = re.fullmatch(r"(\d{4})(-240|-400)?\.(avif|webp)", p.name)
            if m:
                shutil.copy2(p, dst / p.name)
                if p.suffix == ".webp":
                    imgs.add(m.group(1))
    dict_urls, stats = None, None
    # Tua Pek Kong + Guan Yin Ma (000-999 each): text as hashed JSON, pictures as 40 AVIF sheets each
    books = {}
    bdir = Path(__file__).resolve().parent.parent
    for key in ("tpk", "gy"):
        bj, bs = bdir / "dict_books" / f"{key}.json", bdir / f"sprites_{key}"
        if bj.exists() and bs.is_dir():
            b = bj.read_bytes()
            books[key] = f"data/book-{key}.{h8(b)}.json"
            (out / "data").mkdir(exist_ok=True)
            (out / books[key]).write_bytes(b)
            shutil.copytree(bs, out / "img" / key)
    text = load_text(Path(a.text)) if a.text else {}
    if a.dict or imgs or text:
        lines = build_dict(Path(a.dict) if a.dict else None, imgs, text)
        # extra wordings from the 4D Lucky Book copy of the same book: an 8th, search-only field
        altf = Path(__file__).resolve().parent.parent / "dict_books" / "wz_alt.json"
        if lines and altf.exists():
            alt = json.loads(altf.read_text(encoding="utf-8"))
            lines = [l + "|" * max(0, 6 - l.count("|")) + "|" + alt[l[:4]] if l[:4] in alt else l for l in lines]
        if lines:
            dict_urls, stats = [], {"pictures": len(imgs), "chunks": [0] * 10, "zh": 0, "en": 0, "ms": 0, "ta": 0}
            for k in range(10):
                part = [l for l in lines if l[0] == str(k)]
                stats["chunks"][k] = len(part)
                for l in part:
                    f = l.split("|")
                    for key, i in (("zh", 2), ("en", 3), ("ms", 4), ("ta", 5)):
                        stats[key] += bool(f[i])
                if part:
                    b = "\n".join(part).encode()
                    name = f"data/dict-{k}.{h8(b)}.txt"
                    (out / name).write_bytes(b)
                    dict_urls.append(name)
                else:
                    dict_urls.append(None)

    html = Path(a.template).read_text()
    jkd = Path(__file__).with_name("brand") / "fonts" / "jakarta-digits.woff2"   # 4 KB digits-only cut for the header strip
    jkd_name = "assets/jkd." + h8(jkd.read_bytes()) + ".woff2"
    (out / "assets").mkdir(exist_ok=True)
    (out / jkd_name).write_bytes(jkd.read_bytes())
    html = html.replace("__JKD__", jkd_name)
    html = (html.replace("__DATAURL__", res_name).replace("__SITEURL__", a.site)
                .replace("__UPDTXT__", "Updated " + __import__("datetime").datetime.now(__import__("datetime").timezone(__import__("datetime").timedelta(hours=8))).strftime("%-d %b %Y, %-I:%M%p").replace("AM", "am").replace("PM", "pm") + " MYT").replace("__SPECIAL__", json.dumps([d.replace("-", "") for d in json.loads((Path(__file__).with_name("special_draws.json")).read_text())["dates"]])).replace("__DICTURL__", json.dumps(dict_urls)).replace("__BOOKS__", json.dumps(books)).replace("__DICTSTATS__", json.dumps(stats)).replace("__DICT__", '""').replace("__DICTIMG__", "{}"))
    from urllib.parse import urlparse
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import seo_pages as SP
    import seo_copy as SC
    SP.LANG_META.update(SC.META)
    site = a.site.rstrip("/") + "/"
    base = urlparse(site).path or "/"
    data = json.loads(res)
    lastiso = max(r.split(",")[0] for v in data.values() for r in v.split("|"))
    lastiso = f"{lastiso[:4]}-{lastiso[4:6]}-{lastiso[6:]}"
    url = {"en": site, "ms": site + "ms/", "zh": site + "zh/", "ta": site + "ta/"}
    hl = {"en": "en", "ms": "ms", "zh": "zh-Hans", "ta": "ta"}
    alts = [(hl[k], v) for k, v in url.items()] + [("x-default", site)]
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alts)
    h1 = {"en": "Malaysia 4D results tonight — Magnum, Sports Toto, Da Ma Cai", "ms": "Keputusan 4D Malaysia malam ini — Magnum, Sports Toto, Da Ma Cai",
          "zh": "今晚马来西亚万字成绩 — 万能、多多、大马彩", "ta": "இன்றிரவு மலேசியா 4D முடிவுகள் — Magnum, Sports Toto, Da Ma Cai"}
    h1 = SC.H1
    locale = {"en": "en_MY", "ms": "ms_MY", "zh": "zh_MY", "ta": "ta_MY"}
    titles = {k: v[0] for k, v in SP.LANG_META.items()}
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "4D Malam Ini", "url": site, "inLanguage": ["en", "ms", "zh-Hans", "ta"],
           "potentialAction": {"@type": "SearchAction", "target": site + "?n={search_term_string}", "query-input": "required name=search_term_string"}},
          {"@context": "https://schema.org", "@type": "Organization", "name": "4D Malam Ini", "url": site, "logo": site + "icon-512.png", "sameAs": ["https://t.me/ssgsales"], "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "url": "https://t.me/ssgsales", "availableLanguage": ["en", "ms", "zh", "ta"]}}]
    ldjson = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>' for x in ld)
    html = (html.replace("__BASE__", base).replace("__HREFLANG__", hreflang).replace("__LDJSON__", ldjson)
                .replace("__LASTISO__", lastiso).replace("__TITLES__", json.dumps(titles, ensure_ascii=False)))
    xf = Path(a.results).with_name("extras.json")
    html = prerender_latest(html, data, json.loads(xf.read_text(encoding="utf-8")) if xf.exists() else {})
    html = prerender_static(html, data)
    html = prerender_spd(html)
    mini = shutil.which("html-minifier-terser") or next((str(p) for p in [Path(__file__).resolve().parent.parent / "node_modules/.bin/html-minifier-terser"] if p.exists()), None)
    if not mini:
        print("  ! html-minifier-terser not found: pages left unminified (npm i -g html-minifier-terser)")
    import themes as TH                      # Black / Day / Starry Night switch (see themes.py)
    sky_url = TH.write_fragment(out)
    for lang in ("en", "ms", "zh", "ta"):
        title, desc = SP.LANG_META[lang]
        page = (prerender_lang(html, lang).replace("__HTMLLANG__", SP.HTML_LANG[lang]).replace("__CANON__", url[lang])
                .replace("__TITLE__", H.escape(title)).replace("__DESC__", H.escape(desc)).replace("__OGLOCALE__", locale[lang])
                .replace("__H1__", H.escape(h1[lang])).replace("<!--SEO-->", SC.block(lang) + SC.faq_ld(lang)).replace('id="nav-guide" href="info/"', f'id="nav-guide" href="{"" if lang == "en" else lang + "/"}info/"').replace('id="home" href="./"', f'id="home" href="{"./" if lang == "en" else lang + "/"}"')
                .replace('id="lnk-stats" href="4d-statistics/"', f'id="lnk-stats" href="/{"" if lang == "en" else lang + "/"}4d-statistics/"')
                .replace('id="lnk-pop" href="popular-4d-numbers/"', f'id="lnk-pop" href="/{"" if lang == "en" else lang + "/"}popular-4d-numbers/"'))
        page = board_lang(rd_label(page, lang), lang)
        pre_ = "" if lang == "en" else lang + "/"

        # Footer: grouped link columns + company list, built for every language so the in-page
        # language switcher can swap them without a reload (the page's own language is rendered
        # server-side, so it is what crawlers and no-JS visitors get).
        def footcols(lg):
            pf = "" if lg == "en" else lg + "/"
            FG = {
             "en": (("Results", [("Latest results", f"keputusan/{lastiso}/", 0), ("Results archive", "keputusan/", 1), ("Special draws", pf + "special-draw/", 0)]),
                    ("Numbers", [("Check a number", pf + "check-4d-number/", 0), ("4D dictionary", "4d/", 0), ("Popular numbers", pf + "popular-4d-numbers/", 0), ("4D statistics", pf + "4d-statistics/", 0)]),
                    ("About", [("Info centre", pf + "info/", 0), ("How to play", pf + "guide/", 0), ("About us", pf + "about/", 0), ("Data policy", "data-policy/", 0), ("Sitemap", pf + "sitemap/", 0)])),
             "ms": (("Keputusan", [("Keputusan terkini", f"keputusan/{lastiso}/", 0), ("Arkib keputusan", "keputusan/", 1), ("Cabutan khas", pf + "special-draw/", 0)]),
                    ("Nombor", [("Semak nombor", pf + "check-4d-number/", 0), ("Kamus 4D 万字图", "4d/", 0), ("Nombor popular", pf + "popular-4d-numbers/", 0), ("Statistik 4D", pf + "4d-statistics/", 0)]),
                    ("Maklumat", [("Pusat info", pf + "info/", 0), ("Panduan 4D", pf + "guide/", 0), ("Tentang kami", pf + "about/", 0), ("Dasar data", "data-policy/", 0), ("Peta laman", pf + "sitemap/", 0)])),
             "zh": (("成绩", [("最新成绩", f"keputusan/{lastiso}/", 0), ("成绩记录", "keputusan/", 1), ("特别开彩", pf + "special-draw/", 0)]),
                    ("号码", [("查号码", pf + "check-4d-number/", 0), ("万字图", "4d/", 0), ("热门号码", pf + "popular-4d-numbers/", 0), ("万字统计", pf + "4d-statistics/", 0)]),
                    ("关于", [("资讯中心", pf + "info/", 0), ("玩法指南", pf + "guide/", 0), ("关于我们", pf + "about/", 0), ("数据政策", "data-policy/", 0), ("网站地图", pf + "sitemap/", 0)])),
             "ta": (("முடிவுகள்", [("சமீபத்திய முடிவுகள்", f"keputusan/{lastiso}/", 0), ("முடிவுகள் காப்பகம்", "keputusan/", 1), ("சிறப்புக் குலுக்கல்", pf + "special-draw/", 0)]),
                    ("எண்கள்", [("எண் சரிபார்", pf + "check-4d-number/", 0), ("4D அகராதி", "4d/", 0), ("பிரபல எண்கள்", pf + "popular-4d-numbers/", 0), ("4D புள்ளிவிவரம்", pf + "4d-statistics/", 0)]),
                    ("தகவல்", [("தகவல் மையம்", pf + "info/", 0), ("விளையாடும் முறை", pf + "guide/", 0), ("எங்களைப் பற்றி", pf + "about/", 0), ("தரவுக் கொள்கை", "data-policy/", 0), ("தள வரைபடம்", pf + "sitemap/", 0)])),
            }[lg]
            SL = ["magnum-4d-result", "da-ma-cai-result", "sports-toto-result", "gd-lotto-result", "9-lotto-result",
                  "singapore-4d-result", "cash-sweep-result", "sabah-88-4d-result", "sandakan-4d-result", "super-j3-j9-result"]
            CN = {"zh": ["万能", "大马彩", "多多", "豪龙", "9 Lotto", "新加坡万字", "砂拉越大万", "沙巴88", "山打根", "Super J3 & J9"]}.get(
                lg, ["Magnum 4D", "Da Ma Cai", "Sports Toto", "GD Lotto", "9 Lotto", "Singapore 4D", "Cash Sweep", "Sabah 88", "Sandakan 4D", "Super J3 & J9"])
            CO = list(zip(CN, SL))
            COH = {"en": "By company", "ms": "Ikut syarikat", "zh": "各公司成绩", "ta": "நிறுவனம் வாரியாக"}[lg]
            out = "".join(f'<nav><b>{H.escape(h)}</b>' + "".join(f'<a href="/{u}"{" data-cal" if c else ""}>{H.escape(t)}</a>' for t, u, c in ls) + "</nav>" for h, ls in FG)
            return out + f'<nav class="co"><b>{H.escape(COH)}</b><div>' + "".join(f'<a href="/{pf}{u}/">{H.escape(t)}</a>' for t, u in CO) + "</div></nav>"

        page = (page.replace("<!--FOOTLINKS-->", footcols(lang))
                    .replace("__FLINKS__", json.dumps(
                        {lg: SP.localize(footcols(lg), lg) for lg in ("en", "ms", "zh", "ta")}, ensure_ascii=False))
                    .replace('href="special-draw/"', f'href="/{pre_}special-draw/"'))
        page = SP.localize(page, lang)
        f = out / ("index.html" if lang == "en" else f"{lang}/index.html")
        f.parent.mkdir(exist_ok=True)
        f.write_text(page)
        if mini:
            subprocess.run([mini, "--collapse-whitespace", "--remove-comments", "--minify-css", "true", "--minify-js", "true",
                            "--remove-redundant-attributes", "-o", str(f), str(f)], check=True)
        # The app script lives in assets/app.<hash>.js (cached forever). It redraws the board after
        # first paint, so the prerender must match its first render (jackpots, 6D, card order,
        # ticker hidden, special-draw pill) or the page shifts: CLS was 0.58 before that (6 Nov).
        f.write_text(external_app(TH.apply(f.read_text(), sky_url), out))
    mark = Path(__file__).with_name("brand").joinpath("mark.svg").read_text().replace("<svg ", '<svg width="40" height="28" aria-hidden="true" ', 1)
    sp = SP.Site(out, site, base, data, lines if (a.dict or imgs or text) else [], mark)
    sp.build()
    import guide_pages as GP
    GP.build(sp)
    import info_pages as IP
    IP.build(sp)
    import about_pages as AP
    AP.build(sp)
    import op_pages as OPP
    OPP.build(sp)
    import special_pages as SDP
    SDP.build(sp)
    import stats_pages as STP
    STP.build(sp)
    import popular_pages as PPP
    PPP.build(sp)
    import check_pages as CKP
    CKP.build(sp)
    import legal_pages as LGP
    LGP.build(sp)
    import sitemap_pages as SMP
    SMP.build(sp)
    # IndexNow: the key file must be readable at https://host/<key>.txt
    kp = Path(__file__).parent / "indexnow.key"
    if kp.exists():
        k = kp.read_text().strip()
        (out / f"{k}.txt").write_text(k)
        print(f"  IndexNow key file: /{k}.txt")
    n_urls = sp.sitemap(alts)
    print(f"  SEO pages: {len(sp.urls)} static pages, {n_urls} URLs in sitemap index, robots.txt, 404.html")
    for fn, cnt in getattr(sp, "sitemap_groups", []):
        print(f"    {fn:26} {cnt:6} urls")

    version = h8((out / "index.html").read_bytes() + res + json.dumps(dict_urls).encode() + json.dumps(books).encode())
    (out / "sw.js").write_text(SW.replace("__V__", version))
    (out / "manifest.webmanifest").write_text(json.dumps({
        "name": "4D Malam Ini", "short_name": "4D Malam Ini", "lang": "ms", "start_url": "./", "scope": "./",
        "description": "Keputusan 4D Malaysia malam ini, sejarah 5 tahun dan 万字图.",
        "display": "standalone", "background_color": "#07142B", "theme_color": "#07142B",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
                  {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False))
    icons(out)
    if imgs:
        print(f"  img/d2/  {len(imgs)} pictures in sprite sheets, {sum(f.stat().st_size for f in (out / 'img' / 'd2').rglob('*.avif'))/1048576:.1f} MB on server")
    live = {k: "|".join(v.split("|")[-3:]) for k, v in data.items()}
    xf = Path(a.results).with_name("extras.json")  # jackpots, Toto 5D/6D/lotto, blank slots (written by fetch_results.py)
    if xf.exists():
        xj = json.loads(xf.read_text(encoding="utf-8"))
        live["X"] = {d: xj[d] for d in sorted(xj)[-4:]}
    (out / "live.json").write_text(json.dumps(live, separators=(",", ":")))
    opyear = "\n".join(
        f"/{pf}{sl}/20*\n  Cache-Control: public, max-age=86400, stale-while-revalidate=604800"
        for pf in ("", "ms/", "zh/", "ta/")
        for sl in ("magnum-4d-result", "da-ma-cai-result", "sports-toto-result", "gd-lotto-result",
                   "9-lotto-result", "singapore-4d-result", "cash-sweep-result", "sabah-88-4d-result", "sandakan-4d-result",
                   "super-j3-j9-result"))
    (out / "_headers").write_text(HEADERS.replace("__OPYEAR__", opyear))
    (out / ".htaccess").write_text(HTACCESS)
    for p in sorted(out.rglob("*")):
        if p.is_file() and not re.search(r"img/d(?:ict|2)|^4d/|^keputusan/", str(p.relative_to(out))):
            print(f"  {p.relative_to(out)}  {p.stat().st_size/1024:.1f} KB")


SW = """const V="4d-__V__";
self.addEventListener("install",e=>{self.skipWaiting()});
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{const r=e.request,u=new URL(r.url);if(r.method!=="GET"||u.origin!==location.origin)return;
if(/\\/(data|img|assets)\\//.test(u.pathname)){e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok)c.put(r,res.clone());return res}))));return}
e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res}).catch(()=>caches.match(r)))});
"""

HEADERS = """# Cloudflare Pages header rules.
#
# IMPORTANT: Pages does NOT let a later rule override an earlier one. A request matching
# several rules inherits all of them, and a header set twice is JOINED WITH A COMMA. So the
# Cache-Control rules below must not overlap: /* carries security headers only, and every
# path that needs a cache policy gets exactly one rule. Anything left unlisted falls back to
# the Pages default (max-age=0, must-revalidate), which is the safe choice for live pages.
#
# Why this matters: 12,000 archive pages were being served max-age=0, must-revalidate, so
# every repeat visit paid a round trip for a page whose content will never change again.
#
# CDN-Cache-Control is read by Cloudflare ahead of Cache-Control. HTML is not edge-cache
# eligible by default, so it does nothing until a Cache Rule is added in the zone; it is
# harmless until then, and the browser TTL is what does the work today.

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# Past draws: fixed once every company has drawn. Short freshness window so tonight's page
# still catches late results, then a long stale-while-revalidate for the five-year archive.
/keputusan/*
  Cache-Control: public, max-age=600, stale-while-revalidate=86400
  CDN-Cache-Control: public, max-age=3600

# Dictionary and number pages: statistics shift once a day at most.
/4d/*
  Cache-Control: public, max-age=86400, stale-while-revalidate=604800
  CDN-Cache-Control: public, max-age=86400

# Fingerprinted or versioned, safe forever.
/assets/*
  Cache-Control: public, max-age=31536000, immutable
  CDN-Cache-Control: public, max-age=31536000
/img/*
  Cache-Control: public, max-age=31536000, immutable
  CDN-Cache-Control: public, max-age=31536000
/data/*
  Cache-Control: public, max-age=31536000, immutable
  CDN-Cache-Control: public, max-age=31536000

# Reference pages that change rarely.
/info/*
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400
/guide/*
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400
/about/*
  Cache-Control: public, max-age=86400
/privacy/*
  Cache-Control: public, max-age=86400
/terms/*
  Cache-Control: public, max-age=86400
/contact/*
  Cache-Control: public, max-age=86400
/data-policy/*
  Cache-Control: public, max-age=86400
/check-4d-number/*
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400

# Crawler files.
/sitemap.xml
  Cache-Control: public, max-age=3600
/sitemap-main.xml
  Cache-Control: public, max-age=3600
/sitemap-results.xml
  Cache-Control: public, max-age=3600
/sitemap-operators.xml
  Cache-Control: public, max-age=3600
/sitemap-dictionary.xml
  Cache-Control: public, max-age=86400
/robots.txt
  Cache-Control: public, max-age=86400

# Provider-year archives (/magnum-4d-result/2025/ and friends, in four languages). The
# "20*" suffix matches the year pages without matching the operator hub above them, which
# shows tonight's draw and must stay on the default must-revalidate.
__OPYEAR__

# The live surfaces. Never hold these.
/live.json
  Cache-Control: no-store
  CDN-Cache-Control: no-store
/sw.js
  Cache-Control: public, max-age=0, must-revalidate
"""

HTACCESS = """# Compression (Apache)
<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/css application/javascript application/json application/manifest+json image/svg+xml
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css application/javascript application/json application/manifest+json image/svg+xml
</IfModule>
AddType application/manifest+json .webmanifest
AddType image/avif .avif
# Caching: hashed data and images forever, page and service worker always fresh
<IfModule mod_headers.c>
  <FilesMatch "\\.(json|txt|avif|webp|mp4|png|svg)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "(index\\.html|sw\\.js|manifest\\.webmanifest)$">
    Header set Cache-Control "public, max-age=0, must-revalidate"
  </FilesMatch>
</IfModule>
"""

if __name__ == "__main__":
    main()
