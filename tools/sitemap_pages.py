"""HTML sitemap: /sitemap/ (+ /ms/ /zh/ /ta/). Every section of the site on one page,
including each company's results page and the results archive year by year."""
import datetime as dt
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
CO = [("Magnum 4D", "magnum-4d-result", 0), ("Da Ma Cai 1+3D", "da-ma-cai-result", 1), ("Sports Toto 4D", "sports-toto-result", 2),
      ("GD Lotto 4D", "gd-lotto-result", 6), ("9 Lotto 4D", "9-lotto-result", 7), ("Singapore 4D", "singapore-4d-result", 3),
      ("Cash Sweep", "cash-sweep-result", 4), ("Sandakan 4D", "sandakan-4d-result", 5), ("Super J3 & J9", "super-j3-j9-result", 8)]

T = {
 "en": dict(title="Sitemap", crumb="Sitemap", home="Home", h1="Sitemap",
            desc="Every page on 4D Malam Ini: live results, each company's results, the archive by year, the 4D dictionary, statistics and popular numbers.",
            lead="Everything on this site, on one page.",
            g=("Results", "Numbers", "Results archive", "Information"),
            res=[("Live results tonight", ""), ("Results archive", "keputusan/"), ("Special draw dates & results", "special-draw/")],
            num=[("Check a 4D number", "check-4d-number/"), ("4D dictionary · 10,000 numbers", "4d/"), ("Popular 4D numbers", "popular-4d-numbers/"), ("4D statistics", "4d-statistics/")],
            inf=[("Info centre", "info/"), ("How to play 4D", "guide/"), ("About us", "about/"), ("Data & editorial policy", "data-policy/"), ("Contact us", "contact/"), ("Privacy", "privacy/"), ("Terms of use", "terms/")],
            co="Results by company", arch="By year", draws="{n} draws", langs="This page in other languages"),
 "ms": dict(title="Peta Laman", crumb="Peta laman", home="Utama", h1="Peta laman",
            desc="Setiap halaman di 4D Malam Ini: keputusan langsung, keputusan setiap syarikat, arkib mengikut tahun, kamus 4D, statistik dan nombor popular.",
            lead="Semua yang ada di laman ini, dalam satu halaman.",
            g=("Keputusan", "Nombor", "Arkib keputusan", "Maklumat"),
            res=[("Keputusan langsung malam ini", ""), ("Arkib keputusan", "keputusan/"), ("Tarikh & keputusan cabutan khas", "special-draw/")],
            num=[("Semak nombor 4D", "check-4d-number/"), ("Kamus 4D · 10,000 nombor", "4d/"), ("Nombor 4D popular", "popular-4d-numbers/"), ("Statistik 4D", "4d-statistics/")],
            inf=[("Pusat info", "info/"), ("Panduan main 4D", "guide/"), ("Tentang kami", "about/"), ("Dasar data & editorial", "data-policy/"), ("Hubungi kami", "contact/"), ("Privasi", "privacy/"), ("Terma penggunaan", "terms/")],
            co="Keputusan ikut syarikat", arch="Ikut tahun", draws="{n} cabutan", langs="Halaman ini dalam bahasa lain"),
 "zh": dict(title="网站地图", crumb="网站地图", home="首页", h1="网站地图",
            desc="4D Malam Ini 的所有页面：即时成绩、各公司成绩、按年份的成绩记录、万字图、统计、热门号码与网站资讯。",
            lead="本站所有内容，一页看完。",
            g=("成绩", "号码", "成绩记录", "资讯"),
            res=[("今晚即时成绩", ""), ("成绩记录", "keputusan/"), ("特别开彩日期与成绩", "special-draw/")],
            num=[("查万字号码", "check-4d-number/"), ("万字图 · 10,000 个号码", "4d/"), ("热门万字号码", "popular-4d-numbers/"), ("万字统计", "4d-statistics/")],
            inf=[("资讯中心", "info/"), ("万字玩法指南", "guide/"), ("关于我们", "about/"), ("数据与编辑政策", "data-policy/"), ("联系我们", "contact/"), ("隐私", "privacy/"), ("使用条款", "terms/")],
            co="各公司成绩", arch="按年份", draws="{n} 期", langs="其他语言版本"),
 "ta": dict(title="தள வரைபடம்", crumb="தள வரைபடம்", home="முகப்பு", h1="தள வரைபடம்",
            desc="4D Malam Ini-இன் அனைத்துப் பக்கங்களும்: நேரலை முடிவுகள், நிறுவன முடிவுகள், ஆண்டு வாரியான காப்பகம், 4D அகராதி, புள்ளிவிவரம், பிரபல எண்கள், தள தகவல்.",
            lead="இந்தத் தளத்தில் உள்ள அனைத்தும், ஒரே பக்கத்தில்.",
            g=("முடிவுகள்", "எண்கள்", "முடிவுகள் காப்பகம்", "தகவல்"),
            res=[("இன்றிரவு நேரலை முடிவுகள்", ""), ("முடிவுகள் காப்பகம்", "keputusan/"), ("சிறப்புக் குலுக்கல் தேதிகள் & முடிவுகள்", "special-draw/")],
            num=[("4D எண் சரிபார்ப்பு", "check-4d-number/"), ("4D அகராதி · 10,000 எண்கள்", "4d/"), ("பிரபல 4D எண்கள்", "popular-4d-numbers/"), ("4D புள்ளிவிவரம்", "4d-statistics/")],
            inf=[("தகவல் மையம்", "info/"), ("4D விளையாடும் முறை", "guide/"), ("எங்களைப் பற்றி", "about/"), ("தரவு & ஆசிரியர் கொள்கை", "data-policy/"), ("எங்களைத் தொடர்பு கொள்ள", "contact/"), ("தனியுரிமை", "privacy/"), ("பயன்பாட்டு விதிமுறைகள்", "terms/")],
            co="நிறுவனம் வாரியான முடிவுகள்", arch="ஆண்டு வாரியாக", draws="{n} குலுக்கல்", langs="பிற மொழிகளில்"),
}

CSS = """.smp{--mu:#9DB0D3;--cd:#0F1F3D;--ln:#1D3157;--gold:#E9C46B;--ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei","Noto Sans Tamil",sans-serif;font-family:var(--ui)}
.smp h1{font-size:26px;line-height:1.2;letter-spacing:-.4px;margin:6px 0 6px}
.smp .lead{color:var(--mu);margin:0 0 16px;font-size:14px;line-height:1.55}
.smp .lng{display:flex;gap:6px;margin:4px 0 12px}
.smp .lng a{padding:6px 11px;border-radius:999px;border:1px solid var(--ln);text-decoration:none;font-size:12.5px;font-weight:700;color:#C9D4EA}
.smp .lng a[aria-current]{background:#F8F4E8;color:#07142B;border-color:#F8F4E8}
.smp h2{display:flex;align-items:center;gap:9px;font-size:16px;font-weight:700;letter-spacing:-.2px;margin:24px 0 9px}
.smp h2 i{font-style:normal;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:rgba(233,196,107,.14);font-size:14px}
.smp ul{list-style:none;margin:0;padding:0;background:var(--cd);border:1px solid #233862;border-radius:16px;overflow:hidden}
.smp li+li{border-top:1px solid var(--ln)}
.smp li a{display:flex;align-items:center;gap:10px;padding:13px 15px;text-decoration:none;color:#E4EAF6;font-size:14.5px;line-height:1.35}
.smp li a::after{content:"›";margin-left:auto;color:#6F80A3;font-size:17px}
.smp li a img{width:26px;height:26px;flex:none;border-radius:7px;background:#fff;padding:2px;object-fit:contain}
.smp li a .lg{width:26px;height:26px;flex:none;border-radius:7px;background:url(/img/op/tk.webp) 0 0/260px 26px no-repeat}
.smp li a small{margin-left:auto;color:#6F80A3;font-size:12px;font-variant-numeric:tabular-nums}
.smp li a small+::after{margin-left:8px}
.smp .yr{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}
.smp .yr a{display:flex;flex-direction:column;gap:2px;padding:11px 13px;border-radius:14px;background:var(--cd);border:1px solid #233862;text-decoration:none}
.smp .yr b{font:700 17px/1.1 var(--ui);color:#FFE7A3;font-variant-numeric:tabular-nums}
.smp .yr span{font-size:11.5px;color:var(--mu)}
"""


def build(site) -> None:
    from collections import Counter
    import hashlib
    yrs = Counter(d[:4] for d in site.dates)
    css_name = "assets/sm." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / "assets").mkdir(exist_ok=True)
    (site.out / css_name).write_text(CSS)
    path = lambda l: LANGS[l][1] + "sitemap/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}sitemap/">'
    names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
    for lang, x in T.items():
        hl, pre = LANGS[lang]
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        li = lambda items, p=True: "<ul>" + "".join(f'<li><a href="{site.u((pre if p else "") + u)}">{esc(t)}</a></li>' for t, u in items) + "</ul>"
        res = "<ul>" + "".join(f'<li><a href="{site.u(pre if u == "" else u)}">{esc(t)}</a></li>' for t, u in [(x["res"][0][0], ""), (x["res"][1][0], "keputusan/")]) \
            + f'<li><a href="{site.u(pre + "special-draw/")}">{esc(x["res"][2][0])}</a></li></ul>'
        num = "<ul>" + "".join(
            f'<li><a href="{site.u(u if u == "4d/" else pre + u)}">{esc(t)}</a></li>' for t, u in x["num"]) + "</ul>"
        inf = "<ul>" + "".join(f'<li><a href="{site.u((pre if u != "data-policy/" else "") + u)}">{esc(t)}</a></li>' for t, u in x["inf"]) + "</ul>"
        co = "<ul>" + "".join(f'<li><a href="{site.u(pre + u + "/")}"><span class="lg" style="background-position:{-i * 26}px 0"></span>{esc(t)}</a></li>' for t, u, i in CO) + "</ul>"
        lastof = {d[:4]: d for d in sorted(site.dates)}
        ar = '<div class="yr">' + "".join(
            f'<a href="{site.u(f"keputusan/{y}/") if lang == "ms" else site.u(pre) + "?d=" + lastof[y]}"><b>{y}</b><span>{esc(x["draws"].format(n=n))}</span></a>'
            for y, n in sorted(yrs.items(), reverse=True)) + "</div>"
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        body = (f'<div class="smp">{lng}{bc}<h1>{esc(x["h1"])}</h1><p class="lead">{esc(x["lead"])}</p>'
                f'<h2><i>🔴</i>{esc(x["g"][0])}</h2>{res}'
                f'<h2><i>🏢</i>{esc(x["co"])}</h2>{co}'
                f'<h2><i>🔢</i>{esc(x["g"][1])}</h2>{num}'
                f'<h2><i>🗓️</i>{esc(x["g"][2])}</h2>{ar}'
                f'<h2><i>ℹ️</i>{esc(x["g"][3])}</h2>{inf}</div>')
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"], body, lang=hl, ld=[bld],
                  head=f'<link rel="stylesheet" href="{site.u(css_name)}">' + alts)
