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

OPS = {"Magnum 4D": "M", "Sports Toto 4D": "T", "Da Ma Cai 1+3D": "D", "GD Lotto 4D": "G", "9 Lotto 4D": "N", "9 Lotto 4D 9PM": "N", "Super J3 3PM": "J", "Super J9 9PM": "K", "Singapore 4D": "S", "Sarawak Cash Sweep": "C", "Sandakan 4D": "H"}


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


def prerender_latest(html: str, data: dict) -> str:
    """Write the results board (classic result slips, official draw order) into the page; the page script redraws it in the visitor's language."""
    import datetime
    board = [("M", "Magnum 4D", "#E9C46B"), ("D", "Da Ma Cai", "#4C8DFF"), ("T", "Sports Toto", "#FF5A5F"), ("S", "Singapore 4D", "#38BDF8"), ("C", "Cash Sweep", "#4ADE80"), ("H", "Sandakan 4D", "#FACC15"), ("G", "GD Lotto", "#F27BA5"), ("N", "9 Lotto", "#2EC4B6"), ("J", "Super J3 3pm", "#A78BFA"), ("K", "Super J9 9pm", "#FB923C")]
    zh = {"M": "万能", "D": "大马彩", "T": "多多", "G": "豪龙", "N": "", "J": "下午3点", "K": "晚上9点", "S": "新加坡万字", "C": "砂拉越大万", "H": "山打根"}
    hc = {"M": "#FFF200", "D": "#000080", "T": "#C00000", "G": "#B0121B", "N": "#0E8F86", "J": "#5B21B6", "K": "#C2410C", "S": "#B91C2C", "C": "#0B7A3B", "H": "#14532D"}
    fd = lambda d: datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("%a, %-d %b %Y")
    cdf = lambda d: datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("(%a) %d-%b-%Y")
    nb = lambda n: f'<button type="button" data-n="{n}">{n}</button>'
    head = lambda k, name, sub: (f'<div class="sh"><span class="lgw">{('<img class="opl" src="img/op/n-s.webp" width="46" height="46" alt="9 Lotto">' if k == "N" else f'<img class="opl" src="img/op/{k.lower()}{"-n" if k in "DT" else ""}.webp?v=4" width="40" height="40" alt="">')}</span>'
                                 f'<div class="sht"><b>{name} <i>{zh[k]}</i></b><small>{sub}</small></div></div>')
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
        cards.append(f'<article class="rc slip k-{k}" id="rc-{k}" {stl}>{head(k, name, cdf(d) + (f" #{no}" if no else ""))}{lb}'
                     f'<div class="s3">{"".join(nb(x) for x in n[:3])}</div>'
                     f'<div class="sec">Special<em>特别奖</em></div><div class="s5">{"".join(nb(x) for x in sorted(n[3:13]))}</div>'
                     f'<div class="sec">Consolation<em>安慰奖</em></div><div class="s5">{"".join(nb(x) for x in sorted(n[13:]))}</div></article>')
    jump = "".join(f'<a href="#rc-{k}" style="--c:{c}"><i></i>{name}</a>' for k, name, c in board)
    assert "<!--BOARD-->" in html
    html = html.replace("<!--BOARD-->", "".join(cards)).replace('<nav class="jump" id="rjump" aria-label="Jump to company"></nav>', f'<nav class="jump" id="rjump" aria-label="Jump to company">{jump}</nav>')
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


def icons(out: Path) -> None:
    """Copy the 4D Malam Ini brand files (favicon, app icons, share image) into the site root."""
    brand = Path(__file__).with_name("brand")
    for f in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "og-image.jpg"):
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
    text = load_text(Path(a.text)) if a.text else {}
    if a.dict or imgs or text:
        lines = build_dict(Path(a.dict) if a.dict else None, imgs, text)
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
    html = (html.replace("__DATAURL__", res_name).replace("__SITEURL__", a.site)
                .replace("__UPDTXT__", "Updated " + __import__("datetime").datetime.now(__import__("datetime").timezone(__import__("datetime").timedelta(hours=8))).strftime("%-d %b %Y, %-I:%M%p").replace("AM", "am").replace("PM", "pm") + " MYT").replace("__SPECIAL__", json.dumps([d.replace("-", "") for d in json.loads((Path(__file__).with_name("special_draws.json")).read_text())["dates"]])).replace("__DICTURL__", json.dumps(dict_urls)).replace("__DICTSTATS__", json.dumps(stats)).replace("__DICT__", '""').replace("__DICTIMG__", "{}"))
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
    html = prerender_latest(html, data)
    html = prerender_static(html, data)
    mini = shutil.which("html-minifier-terser") or next((str(p) for p in [Path(__file__).resolve().parent.parent / "node_modules/.bin/html-minifier-terser"] if p.exists()), None)
    if not mini:
        print("  ! html-minifier-terser not found: pages left unminified (npm i -g html-minifier-terser)")
    for lang in ("en", "ms", "zh", "ta"):
        title, desc = SP.LANG_META[lang]
        page = (prerender_lang(html, lang).replace("__HTMLLANG__", SP.HTML_LANG[lang]).replace("__CANON__", url[lang])
                .replace("__TITLE__", H.escape(title)).replace("__DESC__", H.escape(desc)).replace("__OGLOCALE__", locale[lang])
                .replace("__H1__", H.escape(h1[lang])).replace("<!--SEO-->", SC.block(lang) + SC.faq_ld(lang)).replace('id="nav-guide" href="info/"', f'id="nav-guide" href="{"" if lang == "en" else lang + "/"}info/"').replace('id="home" href="./"', f'id="home" href="{"./" if lang == "en" else lang + "/"}"')
                .replace('id="lnk-stats" href="4d-statistics/"', f'id="lnk-stats" href="/{"" if lang == "en" else lang + "/"}4d-statistics/"')
                .replace('id="lnk-pop" href="popular-4d-numbers/"', f'id="lnk-pop" href="/{"" if lang == "en" else lang + "/"}popular-4d-numbers/"'))
        pre_ = "" if lang == "en" else lang + "/"
        # Footer: grouped link columns + company list
        FG = {
         "en": (("Results", [("Latest results", f"keputusan/{lastiso}/", 0), ("Results archive", "keputusan/", 1), ("Special draws", pre_ + "special-draw/", 0)]),
                ("Numbers", [("4D dictionary", "4d/", 0), ("Popular numbers", pre_ + "popular-4d-numbers/", 0), ("4D statistics", pre_ + "4d-statistics/", 0)]),
                ("About", [("Info centre", pre_ + "info/", 0), ("How to play", pre_ + "guide/", 0), ("About us", pre_ + "about/", 0), ("Data policy", "data-policy/", 0), ("Sitemap", pre_ + "sitemap/", 0)])),
         "ms": (("Keputusan", [("Keputusan terkini", f"keputusan/{lastiso}/", 0), ("Arkib keputusan", "keputusan/", 1), ("Cabutan khas", pre_ + "special-draw/", 0)]),
                ("Nombor", [("Kamus 4D 万字图", "4d/", 0), ("Nombor popular", pre_ + "popular-4d-numbers/", 0), ("Statistik 4D", pre_ + "4d-statistics/", 0)]),
                ("Maklumat", [("Pusat info", pre_ + "info/", 0), ("Panduan 4D", pre_ + "guide/", 0), ("Tentang kami", pre_ + "about/", 0), ("Dasar data", "data-policy/", 0), ("Peta laman", pre_ + "sitemap/", 0)])),
         "zh": (("成绩", [("最新成绩", f"keputusan/{lastiso}/", 0), ("成绩记录", "keputusan/", 1), ("特别开彩", pre_ + "special-draw/", 0)]),
                ("号码", [("万字图", "4d/", 0), ("热门号码", pre_ + "popular-4d-numbers/", 0), ("万字统计", pre_ + "4d-statistics/", 0)]),
                ("关于", [("资讯中心", pre_ + "info/", 0), ("玩法指南", pre_ + "guide/", 0), ("关于我们", pre_ + "about/", 0), ("数据政策", "data-policy/", 0), ("网站地图", pre_ + "sitemap/", 0)])),
         "ta": (("முடிவுகள்", [("சமீபத்திய முடிவுகள்", f"keputusan/{lastiso}/", 0), ("முடிவுகள் காப்பகம்", "keputusan/", 1), ("சிறப்புக் குலுக்கல்", pre_ + "special-draw/", 0)]),
                ("எண்கள்", [("4D அகராதி", "4d/", 0), ("பிரபல எண்கள்", pre_ + "popular-4d-numbers/", 0), ("4D புள்ளிவிவரம்", pre_ + "4d-statistics/", 0)]),
                ("தகவல்", [("தகவல் மையம்", pre_ + "info/", 0), ("விளையாடும் முறை", pre_ + "guide/", 0), ("எங்களைப் பற்றி", pre_ + "about/", 0), ("தரவுக் கொள்கை", "data-policy/", 0), ("தள வரைபடம்", pre_ + "sitemap/", 0)])),
        }[lang]
        CO = [("Magnum 4D", "magnum-4d-result"), ("Da Ma Cai", "da-ma-cai-result"), ("Sports Toto", "sports-toto-result"), ("GD Lotto", "gd-lotto-result"),
              ("9 Lotto", "9-lotto-result"), ("Singapore 4D", "singapore-4d-result"), ("Cash Sweep", "cash-sweep-result"), ("Sandakan 4D", "sandakan-4d-result"),
              ("Super J3 & J9", "super-j3-j9-result")]
        COH = {"en": "By company", "ms": "Ikut syarikat", "zh": "各公司成绩", "ta": "நிறுவனம் வாரியாக"}[lang]
        cols = "".join(f'<nav><b>{H.escape(h)}</b>' + "".join(f'<a href="/{u}"{" data-cal" if c else ""}>{H.escape(t)}</a>' for t, u, c in ls) + "</nav>" for h, ls in FG)
        cols += f'<nav class="co"><b>{H.escape(COH)}</b><div>' + "".join(f'<a href="/{pre_}{u}/">{H.escape(t)}</a>' for t, u in CO) + "</div></nav>"
        page = page.replace("<!--FOOTLINKS-->", cols).replace('href="special-draw/"', f'href="/{pre_}special-draw/"')
        page = SP.localize(page, lang)
        f = out / ("index.html" if lang == "en" else f"{lang}/index.html")
        f.parent.mkdir(exist_ok=True)
        f.write_text(page)
        if mini:
            subprocess.run([mini, "--collapse-whitespace", "--remove-comments", "--minify-css", "true", "--minify-js", "true",
                            "--remove-redundant-attributes", "-o", str(f), str(f)], check=True)
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
    import sitemap_pages as SMP
    SMP.build(sp)
    n_urls = sp.sitemap(alts)
    print(f"  SEO pages: {len(sp.urls)} static pages, sitemap.xml with {n_urls} URLs, robots.txt, 404.html")

    version = h8((out / "index.html").read_bytes() + res + json.dumps(dict_urls).encode())
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
    (out / "_headers").write_text(HEADERS)
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

HEADERS = """/index.html
  Cache-Control: public, max-age=0, must-revalidate
/sw.js
  Cache-Control: public, max-age=0, must-revalidate
/live.json
  Cache-Control: public, max-age=0, must-revalidate
/data/*
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=31536000, immutable
/assets/*
  Cache-Control: public, max-age=31536000, immutable
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
