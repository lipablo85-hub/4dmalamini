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

OPS = {"Magnum 4D": "M", "Sports Toto 4D": "T", "Da Ma Cai 1+3D": "D", "GD Lotto 4D": "G", "9 Lotto 4D": "N", "9 Lotto 4D 9PM": "P"}


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
    """Write the results board (each company's latest full result, Special/Consolation ascending) into the page."""
    import datetime
    board = [("M", "Magnum 4D", "#E9C46B"), ("D", "Da Ma Cai", "#4C8DFF"), ("T", "Sports Toto", "#FF5A5F"), ("G", "GD Lotto", "#F27BA5"), ("N", "9 Lotto 7pm", "#2EC4B6"), ("P", "9 Lotto 9pm", "#2EC4B6")]
    fd = lambda d: datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("%a, %-d %b %Y")
    nb = lambda n, lab="": f'<button type="button" data-n="{n}">' + (f"<small>{lab}</small>" if lab else "") + f'<span class="mono">{n}</span></button>'
    cards, last = [], ""
    for k, name, c in board:
        if k not in data:
            cards.append(f'<article class="rc soon" id="rc-{k}" style="--c:{c}"><header><b><img class="opl" src="img/op/{k.lower()}.webp" width="32" height="32" alt="">{name}</b><span>Soon</span></header><div class="rb">Results coming soon</div></article>')
            continue
        d, no, dg = data[k].split("|")[-1].split(",")
        last = max(last, d)
        n = [dg[i:i + 4] for i in range(0, 92, 4)]
        cards.append(f'<article class="rc" id="rc-{k}" style="--c:{c}"><header><b><img class="opl" src="img/op/{k.lower()}.webp" width="32" height="32" alt="">{name}</b><span>{fd(d)}' + (f" · #{no}" if no else "") + '</span></header><div class="rb">'
                     f'<div class="r3">{nb(n[0], "1st Prize")}{nb(n[1], "2nd Prize")}{nb(n[2], "3rd Prize")}</div>'
                     f'<div class="rl"><span>Special</span></div><div class="r5">{"".join(nb(x) for x in sorted(n[3:13]))}</div>'
                     f'<div class="rl"><span>Consolation</span></div><div class="r5">{"".join(nb(x) for x in sorted(n[13:]))}</div></div></article>')
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
                .replace("__DICTURL__", json.dumps(dict_urls)).replace("__DICTSTATS__", json.dumps(stats)).replace("__DICT__", '""').replace("__DICTIMG__", "{}"))
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
                .replace("__H1__", H.escape(h1[lang])).replace("<!--SEO-->", SC.block(lang) + SC.faq_ld(lang)).replace('id="nav-guide" href="guide/"', f'id="nav-guide" href="{"" if lang == "en" else lang + "/"}guide/"').replace('id="home" href="./"', f'id="home" href="{"./" if lang == "en" else lang + "/"}"'))
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
