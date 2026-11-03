"""Static, crawlable pages for 4D Malam Ini: one page per 4D number (10,000) and per draw date,
hub pages linking to them, language versions of the home page, sitemap.xml, robots.txt and 404.html.
Called from build.py. Pure standard library."""
import datetime as dt
import html as H
import json
import re
from collections import defaultdict
from pathlib import Path

OPS = [("M", "Magnum 4D", "万能", "#E9C46B"), ("D", "Da Ma Cai", "大马彩", "#4C8DFF"), ("T", "Sports Toto", "多多", "#FF5A5F"), ("G", "GD Lotto", "豪龙", "#F27BA5"), ("N", "9 Lotto", "9 Lotto", "#2EC4B6")]
PRIZE = {1: ("Hadiah Pertama", "1st Prize", "头奖"), 2: ("Hadiah Kedua", "2nd Prize", "二奖"), 3: ("Hadiah Ketiga", "3rd Prize", "三奖"),
         4: ("Istimewa", "Special", "特别奖"), 5: ("Saguhati", "Consolation", "安慰奖")}
HARI = ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"]
BULAN = ["Januari", "Februari", "Mac", "April", "Mei", "Jun", "Julai", "Ogos", "September", "Oktober", "November", "Disember"]
LANG_META = {
    "en": ("4D Malam Ini — Malaysia 4D Results Tonight, 5-Year History & 4D Dictionary",
           "Tonight's Magnum, Sports Toto and Da Ma Cai 4D results. Check any number against 5 years of draws and look it up in the 万字图 4D dictionary. English, BM, 中文, தமிழ்."),
    "ms": ("4D Malam Ini — Keputusan 4D Malaysia Malam Ini, Sejarah 5 Tahun & Kamus 4D",
           "Keputusan 4D Magnum, Sports Toto dan Da Ma Cai malam ini. Semak mana-mana nombor dengan rekod 5 tahun dan cari maksudnya dalam kamus 4D 万字图."),
    "zh": ("4D Malam Ini — 今晚万字成绩、5年中奖历史与万字图",
           "今晚万能、多多、大马彩万字成绩。查询任何号码过去5年的中奖记录，并在万字图查看号码含义。"),
    "ta": ("4D Malam Ini — இன்றிரவு மலேசியா 4D முடிவுகள், 5 ஆண்டு வரலாறு & 4D அகராதி",
           "இன்றிரவு Magnum, Sports Toto, Da Ma Cai 4D முடிவுகள். எந்த எண்ணையும் 5 ஆண்டு குலுக்கல்களுடன் சரிபார்த்து, 万字图 4D அகராதியில் பொருளைப் பாருங்கள்."),
}
HTML_LANG = {"en": "en", "ms": "ms", "zh": "zh-Hans", "ta": "ta"}

CSS = """*{box-sizing:border-box}body{margin:0;background:#07142B;color:#F8F4E8;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans","Noto Sans Tamil","PingFang SC","Microsoft YaHei",sans-serif}
a{color:#E9C46B}a:hover{color:#F3D892}:focus-visible{outline:2px solid #E9C46B;outline-offset:2px}
.w{max-width:720px;margin:0 auto;padding:0 16px 48px}
header{border-bottom:1px solid #1A2C50;background:#0A1832}header .w{display:flex;align-items:center;gap:10px;padding:10px 16px}
header a{display:flex;align-items:center;gap:10px;color:#F8F4E8;text-decoration:none;font-weight:800;font-size:17px}
.bc{font-size:13px;color:#A9B4CC;margin:16px 0 6px}.bc a{color:#A9B4CC}
h1{font-size:26px;line-height:1.2;margin:6px 0 4px;letter-spacing:-.3px}h1 small{display:block;font-size:15px;font-weight:600;color:#A9B4CC;margin-top:4px}
h2{font-size:18px;margin:28px 0 10px}
.mono{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;font-weight:800}
.card{background:#0F1F3D;border:1px solid #233862;border-radius:18px;padding:16px;margin-top:14px}
.pic{display:block;width:100%;max-width:360px;aspect-ratio:1/1;border-radius:16px;overflow:hidden;background:#172A4D;margin:14px 0}
.pic img{display:block;width:100%;height:100%;object-fit:cover}
.pic .sp{display:block;width:100%;height:100%;background-size:500% 500%;background-repeat:no-repeat}
dl{display:grid;grid-template-columns:130px 1fr;gap:8px 12px;margin:0}dt{color:#A9B4CC;font-size:13px;font-weight:700}dd{margin:0}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border-radius:14px;background:#E9C46B;color:#07142B;font-weight:800;text-decoration:none;margin-top:14px}
.btn:hover{color:#07142B;background:#F3D892}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:9px 6px;border-bottom:1px solid #1A2C50}th{font-size:12px;color:#A9B4CC}
.sum{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}.sum div{background:#172A4D;border-radius:12px;padding:10px;text-align:center}.sum b{display:block;font-size:22px}.sum span{font-size:12px;color:#A9B4CC}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips a{display:inline-flex;min-height:44px;align-items:center;padding:0 12px;border-radius:10px;background:#172A4D;text-decoration:none;color:#F8F4E8}
.op{border-left:4px solid;padding-left:12px}.top3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:8px}
.top3 a,.g5 a{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:48px;border-radius:12px;background:#172A4D;text-decoration:none;color:#F8F4E8}
.top3 a .mono{font-size:22px}.top3 small{font-size:11px;color:#A9B4CC}
.g5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;margin-top:6px}.g5 a{min-height:44px;font-size:15px}
.lbl{font-size:12px;font-weight:800;color:#A9B4CC;margin-top:12px}
.pn{display:flex;justify-content:space-between;gap:10px;margin-top:24px}.pn a{min-height:44px;display:inline-flex;align-items:center}
.list{columns:2;column-gap:18px;padding:0;list-style:none}.list li{break-inside:avoid;padding:5px 0;border-bottom:1px solid #1A2C50;font-size:14px}
.list a{text-decoration:none;color:#F8F4E8}.list .mono{color:#E9C46B;margin-right:8px}
footer{max-width:720px;margin:0 auto;padding:18px 16px 40px;font-size:12px;color:#A9B4CC;border-top:1px solid #1A2C50}.tgi{position:relative;display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#fff;color:#1877B8;flex:none}.tgi::after{content:"";position:absolute;inset:0;border-radius:50%;border:2px solid #fff;animation:tgp 2s ease-out infinite}.tgi svg{margin-left:-2px;animation:tgf 3s ease-in-out infinite}@keyframes tgp{0%{transform:scale(1);opacity:.8}100%{transform:scale(1.7);opacity:0}}@keyframes tgf{0%,55%,100%{transform:none;opacity:1}70%{transform:translate(9px,-9px) scale(.6);opacity:0}71%{transform:translate(-9px,9px) scale(.6);opacity:0}85%{transform:none;opacity:1}}@media (prefers-reduced-motion:reduce){.tgi::after,.tgi svg{animation:none}}.tg{display:inline-flex;align-items:center;gap:10px;padding-left:7px!important;margin-top:14px;min-height:44px;padding:0 16px;border-radius:999px;background:#1877B8;color:#fff!important;font-weight:800;font-size:14px;text-decoration:none}
@media(max-width:520px){.list{columns:1}dl{grid-template-columns:110px 1fr}}"""


def esc(s: str) -> str:
    return H.escape(s or "", quote=True)


def d8(s: str) -> dt.date:
    return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def tier(j: int) -> int:
    return j + 1 if j < 3 else (4 if j < 13 else 5)


class Site:
    def __init__(self, out: Path, site: str, base: str, data: dict, dict_lines: list, mark_svg: str):
        self.out, self.site, self.base = out, site.rstrip("/") + "/", base
        self.mark = mark_svg
        self.draws = {}            # op -> list of (date8, drawno, [23 nums]) oldest first
        for k, v in data.items():
            rows = []
            for r in v.split("|"):
                d, no, dg = r.split(",")
                rows.append((d, no, [dg[i:i + 4] for i in range(0, 92, 4)]))
            self.draws[k] = rows
        self.dates = sorted({r[0] for rows in self.draws.values() for r in rows})
        self.hits = defaultdict(list)  # number -> [(date8, op, drawno, tier)]
        for k, rows in self.draws.items():
            for d, no, nums in rows:
                for j, n in enumerate(nums):
                    self.hits[n].append((d, k, no, tier(j)))
        self.dict = {}
        for l in dict_lines:
            f = (l.split("|") + [""] * 7)[:7]
            self.dict[f[0]] = {"zh": f[2], "en": f[3], "ms": f[4], "ta": f[5], "img": f[6]}
        self.urls = []             # (path, lastmod)

    # ---------- helpers ----------
    def u(self, path: str) -> str:
        return self.base + path.lstrip("/")

    def page(self, path: str, title: str, desc: str, body: str, lang: str = "ms", ld: list | None = None, lastmod: str | None = None, head: str = "", foot: str | None = None) -> None:
        canon = self.site + path.lstrip("/")
        DEFAULT_FOOT = f"""<footer>Rekod tidak rasmi untuk rujukan. Sahkan dengan syarikat sebelum menuntut hadiah. 21+ · Bukan Islam sahaja · Main secara bertanggungjawab.<br>
<a href="{self.u('')}">Semak nombor</a> · <a href="{self.u('keputusan/')}">Arkib keputusan</a> · <a href="{self.u('4d/')}">Kamus 4D 万字图</a> · <a href="{self.u('guide/')}">Panduan 4D · Guide</a><br><a class="tg" href="https://t.me/ssgsales" target="_blank" rel="noopener"><i class="tgi" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24"><path fill="currentColor" d="M21.9 4.3 18.7 19.4c-.2 1-.9 1.3-1.7.8l-4.8-3.6-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.9 8.9-8c.4-.3-.1-.5-.6-.2L6.5 13.1l-4.7-1.5c-1-.3-1-1 .2-1.5L20.5 3c.9-.3 1.6.2 1.4 1.3Z"/></svg></i><span>Hubungi kami · Contact us · Telegram</span></a></footer>"""
        lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>' for x in (ld or []))
        doc = f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">
<meta name="theme-color" content="#07142B"><link rel="icon" href="{self.u('favicon.svg')}" type="image/svg+xml"><link rel="apple-touch-icon" href="{self.u('apple-touch-icon.png')}">
<link rel="stylesheet" href="{self.u(self.css)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="4D Malam Ini"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{self.site}og-image.jpg"><meta name="twitter:card" content="summary_large_image">{head}{lds}<script async src="https://www.googletagmanager.com/gtag/js?id=G-VMHF911ZT1"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","G-VMHF911ZT1");</script>
</head>
<body><header><div class="w"><a href="{self.u('')}">{self.mark}<span>4D Malam Ini</span></a></div></header>
<main class="w">{body}</main>
{foot if foot is not None else DEFAULT_FOOT}</body></html>"""
        p = self.out / path.lstrip("/")
        if path.endswith("/"):
            p = p / "index.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(doc, encoding="utf-8")
        self.urls.append((canon, lastmod))

    def crumbs(self, items: list) -> tuple[str, dict]:
        html = " › ".join(f'<a href="{self.u(p)}">{esc(n)}</a>' if p is not None else esc(n) for n, p in items)
        ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, **({"item": self.site + p.lstrip("/")} if p is not None else {})} for i, (n, p) in enumerate(items)]}
        return f'<nav class="bc" aria-label="Breadcrumb">{html}</nav>', ld

    def date_ms(self, d8s: str) -> str:
        d = d8(d8s)
        return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"

    # ---------- pages ----------
    def build(self) -> None:
        self.css = "assets/s." + __import__("hashlib").sha256(CSS.encode()).hexdigest()[:8] + ".css"
        (self.out / "assets").mkdir(exist_ok=True)
        (self.out / self.css).write_text(CSS)
        last = self.dates[-1]
        self.result_pages()
        self.number_pages(last)
        self.hubs(last)
        self.not_found()

    def result_pages(self) -> None:
        by = {k: {r[0]: r for r in rows} for k, rows in self.draws.items()}
        for i, d in enumerate(self.dates):
            iso = d8(d).isoformat()
            body_ops, titles = [], []
            for k, name, zh, col in OPS:
                r = by[k].get(d)
                if not r:
                    continue
                _, no, n = r
                titles.append(name)
                a = lambda x: f'<a href="{self.u(f"4d/{x}/")}" class="mono">{x}</a>'
                top = "".join(f'<a href="{self.u(f"4d/{x}/")}"><span class="mono">{x}</span><small>{PRIZE[j + 1][0]}</small></a>' for j, x in enumerate(n[:3]))
                body_ops.append(f'<section class="card op" style="border-left-color:{col}"><h2 style="margin:0">{name} <small style="color:#A9B4CC;font-weight:600">{zh} · Cabutan {esc(no)}</small></h2>'
                                f'<div class="top3">{top}</div><div class="lbl">Istimewa · Special</div><div class="g5">{"".join(a(x) for x in sorted(n[3:13]))}</div>'
                                f'<div class="lbl">Saguhati · Consolation</div><div class="g5">{"".join(a(x) for x in sorted(n[13:]))}</div></section>')
            nav, ld = self.crumbs([("4D Malam Ini", ""), ("Keputusan", "keputusan/"), (self.date_ms(d), None)])
            prev = f'<a href="{self.u(f"keputusan/{d8(self.dates[i - 1]).isoformat()}/")}">‹ {self.date_ms(self.dates[i - 1])}</a>' if i else "<span></span>"
            nxt = f'<a href="{self.u(f"keputusan/{d8(self.dates[i + 1]).isoformat()}/")}">{self.date_ms(self.dates[i + 1])} ›</a>' if i + 1 < len(self.dates) else "<span></span>"
            dd = d8(d)
            title = f"Keputusan 4D {self.date_ms(d)} — {', '.join(titles)} | 4D Malam Ini"
            desc = f"Keputusan penuh 4D {self.date_ms(d)}: " + "; ".join(
                f"{name} {by[k][d][2][0]}, {by[k][d][2][1]}, {by[k][d][2][2]}" for k, name, _, _ in OPS if d in by[k]) + ". Hadiah istimewa dan saguhati."
            body = (f"{nav}<h1>Keputusan 4D {self.date_ms(d)}<small>4D results {dd:%A, %-d %B %Y} · {dd.year}年{dd.month}月{dd.day}日万字成绩</small></h1>"
                    + "".join(body_ops) + f'<div class="pn">{prev}{nxt}</div>')
            self.page(f"keputusan/{iso}/", title, desc, body, "ms", [ld], iso)

    def number_pages(self, last: str) -> None:
        lo, hi = d8(self.dates[0]), d8(self.dates[-1])
        span = f"{BULAN[lo.month - 1][:3]} {lo.year} – {BULAN[hi.month - 1][:3]} {hi.year}"
        for i in range(10000):
            n = f"{i:04d}"
            e = self.dict.get(n, {"zh": "", "en": "", "ms": "", "ta": "", "img": ""})
            hits = sorted(self.hits.get(n, []), reverse=True)
            r = f"{i // 1000}000-{i // 1000}999"
            nav, ld = self.crumbs([("4D Malam Ini", ""), ("Kamus 4D", "4d/"), (r.replace("-", "–"), f"4d/{r}/"), (n, None)])
            name = " · ".join(x for x in (e["zh"], e["en"]) if x)
            pic = ""
            if e["img"]:
                alt = esc(f"4D {n} {e['zh']} {e['en']}".strip())
                o = int(n); c = o % 25
                pic = (f'<span class="pic"><i class="sp" role="img" aria-label="{alt}" style="background-image:url({self.u(f"img/d2/400/{o // 25:03d}.avif")});'
                       f'background-position:{c % 5 * 25}% {c // 5 * 25}%"></i></span>')
            dl = "".join(f"<dt>{lab}</dt><dd{att}>{esc(e[k]) or '—'}</dd>" for k, lab, att in
                         (("zh", "中文", ' lang="zh-Hans"'), ("en", "English", ' lang="en"'), ("ms", "Bahasa Melayu", ""), ("ta", "தமிழ்", ' lang="ta"')))
            cnt = defaultdict(int)
            for h in hits:
                cnt["top" if h[3] <= 3 else ("sp" if h[3] == 4 else "co")] += 1
            opn = {k: nm for k, nm, _, _ in OPS}
            rows = "".join(f'<tr><td><a href="{self.u(f"keputusan/{d8(d).isoformat()}/")}">{self.date_ms(d)}</a></td><td>{opn[k]}</td><td>{PRIZE[t][0]} · {PRIZE[t][1]}</td></tr>' for d, k, no, t in hits)
            hist = (f'<div class="sum"><div><b>{len(hits)}</b><span>Jumlah menang</span></div><div><b>{cnt["top"]}</b><span>Hadiah 1–3</span></div>'
                    f'<div><b>{cnt["sp"]}</b><span>Istimewa</span></div><div><b>{cnt["co"]}</b><span>Saguhati</span></div></div>'
                    + (f'<div class="card" style="padding:4px 12px"><table><thead><tr><th>Tarikh</th><th>Syarikat</th><th>Hadiah</th></tr></thead><tbody>{rows}</tbody></table></div>'
                       if hits else f'<p>{n} tidak menang dalam Magnum, Sports Toto atau Da Ma Cai sejak {span}.</p>'))
            perms = sorted({"".join(p) for p in _perms(n)} - {n})
            box = "".join(f'<a class="mono" href="{self.u(f"4d/{p}/")}">{p}</a>' for p in perms)
            prev, nxt = f"{(i - 1) % 10000:04d}", f"{(i + 1) % 10000:04d}"
            pn = (f'<div class="pn"><a href="{self.u(f"4d/{prev}/")}">‹ {prev} {esc(self.dict.get(prev, {}).get("zh", ""))}</a>'
                  f'<a href="{self.u(f"4d/{nxt}/")}">{nxt} {esc(self.dict.get(nxt, {}).get("zh", ""))} ›</a></div>')
            lastwin = f"Kali terakhir menang {self.date_ms(hits[0][0])} ({opn[hits[0][1]]})." if hits else "Belum menang dalam 5 tahun ini."
            title = f"4D {n}" + (f" {e['zh']}" if e["zh"] else "") + (f" · {e['en']}" if e["en"] else "") + " — 万字图 & sejarah menang | 4D Malam Ini"
            desc = (f"Nombor 4D {n} dalam 万字图: {e['zh']} ({e['en']} / {e['ms']} / {e['ta']}). "
                    f"Menang {len(hits)} kali dalam Magnum, Sports Toto dan Da Ma Cai sejak {span}. {lastwin}")
            body = (f"{nav}<h1><span class=\"mono\">{n}</span> {esc(e['zh'])}<small>{esc(e['en'])}{' · ' + esc(e['ms']) if e['ms'] else ''}</small></h1>{pic}"
                    f'<div class="card"><dl>{dl}</dl></div>'
                    f'<a class="btn" href="{self.u("?n=" + n)}">Semak {n} dalam semua syarikat</a>'
                    f"<h2>Sejarah menang {n} ({span})</h2>{hist}"
                    + (f"<h2>Susunan digit sama (Box) · {len(perms)}</h2><div class=\"chips\">{box}</div>" if perms else "") + pn)
            lastmod = d8(hits[0][0]).isoformat() if hits else None
            self.page(f"4d/{n}/", title, desc, body, "ms", [ld], lastmod)

    def hubs(self, last: str) -> None:
        lastiso = d8(last).isoformat()
        # dictionary hub + range pages
        ranges = []
        for k in range(10):
            r = f"{k}000-{k}999"
            items = "".join(f'<li><a href="{self.u(f"4d/{i:04d}/")}"><span class="mono">{i:04d}</span>{esc(self.dict.get(f"{i:04d}", {}).get("zh", ""))} '
                            f'<span style="color:#A9B4CC">{esc(self.dict.get(f"{i:04d}", {}).get("en", ""))}</span></a></li>' for i in range(k * 1000, k * 1000 + 1000))
            nav, ld = self.crumbs([("4D Malam Ini", ""), ("Kamus 4D", "4d/"), (r.replace("-", "–"), None)])
            self.page(f"4d/{r}/", f"Kamus 4D 万字图 {r.replace('-', '–')} — maksud nombor | 4D Malam Ini",
                      f"Senarai 1,000 nombor 4D {r.replace('-', '–')} dalam 万字图 dengan maksud dalam Bahasa Melayu, English, 中文 dan தமிழ்.",
                      f"{nav}<h1>Kamus 4D 万字图 {r.replace('-', '–')}<small>4D dictionary · 万字图 · 4D அகராதி</small></h1><ul class=\"list\">{items}</ul>", "ms", [ld], lastiso)
            ranges.append(f'<a href="{self.u(f"4d/{r}/")}" class="mono">{r.replace("-", "–")}</a>')
        nav, ld = self.crumbs([("4D Malam Ini", ""), ("Kamus 4D", None)])
        self.page("4d/", "Kamus 4D 万字图 0000–9999 — cari maksud nombor & mimpi | 4D Malam Ini",
                  "Kamus 4D 万字图 lengkap 0000–9999 dengan gambar dan maksud dalam Bahasa Melayu, English, 中文 dan தமிழ். Cari nombor untuk mimpi anda.",
                  f'{nav}<h1>Kamus 4D 万字图 0000–9999<small>4D dictionary · 万字图 · 4D அகராதி</small></h1>'
                  f'<p>10,000 nombor dengan gambar dan maksud dalam empat bahasa. Pilih julat, atau <a href="{self.u("?tab=dict")}">cari dengan perkataan</a>.</p>'
                  f'<div class="chips">{"".join(ranges)}</div>', "ms", [ld], lastiso)
        # results archive hub
        by_year = defaultdict(list)
        for d in reversed(self.dates):
            by_year[d[:4]].append(d)
        secs = "".join(f"<h2>{y}</h2><ul class=\"list\">" + "".join(
            f'<li><a href="{self.u(f"keputusan/{d8(d).isoformat()}/")}">{self.date_ms(d)}</a></li>' for d in ds) + "</ul>" for y, ds in by_year.items())
        nav, ld = self.crumbs([("4D Malam Ini", ""), ("Keputusan", None)])
        self.page("keputusan/", "Arkib keputusan 4D Malaysia — Magnum, Sports Toto, Da Ma Cai | 4D Malam Ini",
                  f"Semua keputusan 4D Magnum, Sports Toto dan Da Ma Cai dari {self.date_ms(self.dates[0])} hingga {self.date_ms(last)}.",
                  f"{nav}<h1>Arkib keputusan 4D<small>4D results archive · 万字成绩档案</small></h1>"
                  f'<p>Terkini: <a href="{self.u(f"keputusan/{lastiso}/")}">{self.date_ms(last)}</a></p>{secs}', "ms", [ld], lastiso)

    def not_found(self) -> None:
        body = (f'<h1>Halaman tidak dijumpai<small>Page not found · 找不到页面 · பக்கம் கிடைக்கவில்லை</small></h1>'
                f'<a class="btn" href="{self.u("")}">Semak nombor 4D</a> <a class="btn" href="{self.u("keputusan/")}" style="background:#172A4D;color:#F8F4E8">Arkib keputusan</a>')
        p = self.out / "404.html"
        self.page("404/", "Halaman tidak dijumpai | 4D Malam Ini", "Halaman ini tiada.", body)
        (self.out / "404" / "index.html").rename(p)
        (self.out / "404").rmdir()
        self.urls.pop()

    def sitemap(self, home_alternates: list) -> None:
        parts = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
        lastiso = d8(self.dates[-1]).isoformat()
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>' for hl, href in home_alternates)
        for hl, href in home_alternates:
            if hl != "x-default":
                parts.append(f"<url><loc>{href}</loc><lastmod>{lastiso}</lastmod>{links}</url>")
        for loc, lm in self.urls:
            parts.append(f"<url><loc>{loc}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
        parts.append("</urlset>")
        (self.out / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8")
        (self.out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {self.site}sitemap.xml\n")
        return len(parts) - 2


def _perms(n: str):
    if len(n) <= 1:
        yield n
        return
    for i, c in enumerate(n):
        for rest in _perms(n[:i] + n[i + 1:]):
            yield c + rest
