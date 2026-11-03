"""About page: /about/ (+ /ms/ /zh/ /ta/). Standalone design (tools/about.css, about.body.html, about.js),
reachable from the Info page's top menu. Text translated in about_i18n.py."""
import hashlib, json, re
from html import escape as esc
from pathlib import Path
import about_i18n as I

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
NAMES = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
HERE = Path(__file__).parent


def build(site) -> None:
    import seo_pages as SP
    css = (HERE / "about.css").read_text(encoding="utf-8") + SP.BN_CSS
    name = "assets/a." + hashlib.sha256(css.encode()).hexdigest()[:8] + ".css"
    (site.out / name).write_text(css, encoding="utf-8")
    body0 = (HERE / "about.body.html").read_text(encoding="utf-8")
    js = (HERE / "about.js").read_text(encoding="utf-8")
    path = lambda l: LANGS[l][1] + "about/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + \
        f'<link rel="alternate" hreflang="x-default" href="{site.site}about/">'
    for lang, (hl, pre) in LANGS.items():
        b = body0
        if lang != "en":
            tr = I.TR[lang]
            b = re.sub(r">(\s*)([^<>]+?)(\s*)<", lambda m: ">" + m.group(1) + tr.get(m.group(2), m.group(2)) + m.group(3) + "<", b)
        langs = "".join(f'<a href="{site.u(path(l))}"' + (' class="on"' if l == lang else "") + f' hreflang="{LANGS[l][0]}">{NAMES[l]}</a>' for l in LANGS)
        rep = {"{{home}}": site.u(pre), "{{root}}": site.u(""), "{{info}}": site.u(pre + "info/"), "{{about}}": site.u(path(lang)),
               "{{guide}}": site.u(pre + "guide/"), "{{img}}": site.u("img/op/"), "{{langs}}": langs}
        for k, v in rep.items():
            b = b.replace(k, v)
        title, desc = I.META[lang]
        canon = site.site + path(lang)
        ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": title, "description": desc, "inLanguage": hl, "url": canon,
              "about": {"@type": "WebSite", "name": "4D Malam Ini", "url": site.site}}
        doc = (f'<!DOCTYPE html><html lang="{hl}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
               f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">{alts}'
               f'<meta name="theme-color" content="#050505"><link rel="icon" href="{site.u("favicon.svg")}" type="image/svg+xml"><link rel="apple-touch-icon" href="{site.u("apple-touch-icon.png")}">'
               f'<meta property="og:type" content="website"><meta property="og:site_name" content="4D Malam Ini"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{site.site}og-image.jpg">'
               f'<link rel="stylesheet" href="{site.u(name)}"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>'
               '<script async src="https://www.googletagmanager.com/gtag/js?id=G-VMHF911ZT1"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","G-VMHF911ZT1");</script>'
               f'</head><body>{b}{site.bnav(path(lang), hl)}{js}</body></html>')
        out = site.out / path(lang) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
        site.urls.append((canon, None))
