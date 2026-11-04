"""Popular 4D numbers hub: /popular-4d-numbers/ (+ /ms/ /zh/ /ta/).
Numbers people play most often and why, grouped by theme, each with its real win record and a link to its number page."""
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}

# group key, icon, numbers [(number, why-popular per language)]
G = [
 ("luck", "🧧", [
   ("8888", {"en": "發發發發 — the strongest prosperity number.", "ms": "發發發發 — nombor kemakmuran paling kuat.", "zh": "發發發發 — 最旺的号码。", "ta": "發發發發 — மிகச் சிறந்த செல்வ எண்."}),
   ("1688", {"en": "一路發發 — prosperity all the way.", "ms": "一路發發 — makmur sepanjang jalan.", "zh": "一路發發 — 生意、车牌最爱。", "ta": "一路發發 — வழி முழுவதும் செழிப்பு."}),
   ("6888", {"en": "六發發發 — smooth 6 with three 8s.", "ms": "六發發發 — angka 6 lancar dengan tiga 8.", "zh": "六發發發 — 六六大顺加三个8。", "ta": "六發發發 — சுமுகமான 6, மூன்று 8."}),
   ("6666", {"en": "六六大順 — everything goes smoothly.", "ms": "六六大順 — semuanya lancar.", "zh": "六六大順 — 事事顺利。", "ta": "六六大順 — அனைத்தும் சுமுகம்."}),
   ("9999", {"en": "長長久久 — long-lasting, and the highest 4D.", "ms": "長長久久 — kekal lama, juga 4D tertinggi.", "zh": "長長久久 — 也是最大的号码。", "ta": "長長久久 — நீண்ட காலம், உயர்ந்த எண்."}),
   ("8168", {"en": "發一路發 — a classic car-plate number.", "ms": "發一路發 — nombor plat klasik.", "zh": "發一路發 — 经典车牌号。", "ta": "發一路發 — பாரம்பரிய தகட்டு எண்."}),
 ]),
 ("love", "❤️", [
   ("1314", {"en": "一生一世 — a whole lifetime.", "ms": "一生一世 — seumur hidup.", "zh": "一生一世 — 纪念日常买。", "ta": "一生一世 — வாழ்நாள் முழுவதும்."}),
   ("5201", {"en": "我愛你 — 520 sounds like 'I love you'.", "ms": "我愛你 — 520 berbunyi 'aku cinta kamu'.", "zh": "我爱你 — 520谐音。", "ta": "我愛你 — 520 'நான் உன்னை காதலிக்கிறேன்'."}),
   ("5211", {"en": "我愛你一一 — the same wish, written differently.", "ms": "我愛你一一 — harapan sama, tulisan lain.", "zh": "我爱你一一 — 另一种写法。", "ta": "我愛你一一 — அதே விருப்பம், வேறு வடிவம்."}),
   ("1413", {"en": "The mirror of 1314.", "ms": "Cermin kepada 1314.", "zh": "1314的倒写。", "ta": "1314-இன் தலைகீழ்."}),
 ]),
 ("repeat", "🔁", [
   ("1111", {"en": "All ones — easiest to remember.", "ms": "Semua 1 — paling mudah diingat.", "zh": "全1 — 最好记。", "ta": "எல்லாம் 1 — நினைவில் எளிது."}),
   ("2222", {"en": "All twos — good things come in pairs.", "ms": "Semua 2 — perkara baik datang berpasangan.", "zh": "全2 — 好事成双。", "ta": "எல்லாம் 2 — இரட்டை அதிர்ஷ்டம்."}),
   ("1234", {"en": "The most played sequence in Malaysia.", "ms": "Turutan paling kerap dimainkan.", "zh": "最多人买的顺子。", "ta": "அதிகம் விளையாடப்படும் வரிசை."}),
   ("4321", {"en": "The mirror of 1234.", "ms": "Cermin kepada 1234.", "zh": "1234的倒顺子。", "ta": "1234-இன் தலைகீழ்."}),
   ("6789", {"en": "步步高升 — climbing to the top.", "ms": "步步高升 — naik ke puncak.", "zh": "步步高升。", "ta": "步步高升 — உச்சிக்கு ஏறுதல்."}),
   ("0000", {"en": "All zeros — rare and dramatic.", "ms": "Semua sifar — jarang dan dramatik.", "zh": "全0 — 罕见又特别。", "ta": "எல்லாம் 0 — அரிது, வித்தியாசம்."}),
 ]),
 ("date", "🎂", [
   ("0101", {"en": "1 January — new year, new start.", "ms": "1 Januari — tahun baharu.", "zh": "1月1日 — 新年新开始。", "ta": "ஜனவரி 1 — புத்தாண்டு."}),
   ("3112", {"en": "31 December — the last day of the year.", "ms": "31 Disember — hari terakhir tahun.", "zh": "12月31日 — 年尾最后一天。", "ta": "டிசம்பர் 31 — ஆண்டின் கடைசி நாள்."}),
   ("3108", {"en": "31 August — Independence Day.", "ms": "31 Ogos — Hari Kemerdekaan.", "zh": "8月31日 — 国庆日。", "ta": "ஆகஸ்ட் 31 — சுதந்திர தினம்."}),
   ("1609", {"en": "16 September — Malaysia Day.", "ms": "16 September — Hari Malaysia.", "zh": "9月16日 — 马来西亚日。", "ta": "செப்டம்பர் 16 — மலேசியா தினம்."}),
 ]),
]

T = {
 "en": dict(title="Popular 4D Numbers: 8888, 1314, 5201 & More", crumb="Popular numbers", home="Home",
            desc="The 4D numbers Malaysians play most: 8888, 1314, 5201, 1688 and more. What each one means, and how many times it has actually been drawn since {s}.",
            h1="Popular 4D numbers", lead="The numbers people buy most often, what they mean, and how often they have really been drawn in {n} draws since {s}.",
            g={"luck": "Luck & prosperity", "love": "Love & anniversaries", "repeat": "Repeats & sequences", "date": "Dates that matter"},
            won="won {n}×", never="not drawn yet", lastw="last {d}", mean="4D dictionary", tops="Most drawn of these",
            note="Popularity is about culture and habit, not odds. Every 4-digit number from 0000 to 9999 has exactly the same chance in every draw, and a popular number shared by many winners pays each of them less. 21+ · Non-Muslims only · Play responsibly.",
            cta="Check any number", stats="See full 4D statistics"),
 "ms": dict(title="Nombor 4D Popular: 8888, 1314, 5201 & Lain-lain", crumb="Nombor popular", home="Utama",
            desc="Nombor 4D paling popular di Malaysia: 8888, 1314, 5201, 1688 dan banyak lagi. Maksud setiap satu dan berapa kali ia benar-benar keluar sejak {s}.",
            h1="Nombor 4D popular", lead="Nombor yang paling kerap dibeli, maksudnya, dan berapa kali ia benar-benar keluar dalam {n} cabutan sejak {s}.",
            g={"luck": "Tuah & kemakmuran", "love": "Cinta & ulang tahun", "repeat": "Berulang & turutan", "date": "Tarikh penting"},
            won="menang {n}×", never="belum keluar", lastw="terakhir {d}", mean="Kamus 4D", tops="Paling kerap keluar",
            note="Populariti berkaitan budaya dan tabiat, bukan peluang menang. Setiap nombor 0000 hingga 9999 mempunyai peluang yang sama dalam setiap cabutan, dan nombor popular yang dibeli ramai orang membahagikan hadiah kepada lebih ramai pemenang. 21+ · Bukan Islam sahaja · Main secara bertanggungjawab.",
            cta="Semak mana-mana nombor", stats="Lihat statistik 4D penuh"),
 "zh": dict(title="热门万字号码：8888、1314、5201 等", crumb="热门号码", home="首页",
            desc="马来西亚最多人买的万字号码：8888、1314、5201、1688 等。每个号码的含义，以及{s}以来真正开出过几次。",
            h1="热门万字号码", lead="最多人买的号码、它们的含义，以及在{s}以来{n}期开彩中真正开出的次数。",
            g={"luck": "旺财与好运", "love": "爱情与纪念日", "repeat": "叠号与顺子", "date": "重要日期"},
            won="中过 {n} 次", never="还没开过", lastw="最近 {d}", mean="万字图", tops="这里面最常开的",
            note="号码热门与否是文化和习惯，不是中奖机率。0000 到 9999 每个号码在每期的机率完全一样；热门号码买的人多，中奖时要分的人也多。仅限21岁或以上非穆斯林 · 理性投注。",
            cta="查询任何号码", stats="查看完整万字统计"),
 "ta": dict(title="பிரபல 4D எண்கள்: 8888, 1314, 5201 மற்றும் பல", crumb="பிரபல எண்கள்", home="முகப்பு",
            desc="மலேசியர்கள் அதிகம் விளையாடும் 4D எண்கள்: 8888, 1314, 5201, 1688. ஒவ்வொன்றின் பொருள், {s} முதல் எத்தனை முறை உண்மையில் வந்துள்ளது.",
            h1="பிரபல 4D எண்கள்", lead="மக்கள் அதிகம் வாங்கும் எண்கள், அவற்றின் பொருள், {s} முதல் {n} குலுக்கல்களில் உண்மையில் எத்தனை முறை வந்தன.",
            g={"luck": "அதிர்ஷ்டம் & செழிப்பு", "love": "காதல் & ஆண்டுவிழா", "repeat": "மீள்வை & வரிசைகள்", "date": "முக்கிய தேதிகள்"},
            won="{n}× வென்றது", never="இன்னும் வரவில்லை", lastw="கடைசி {d}", mean="4D அகராதி", tops="இவற்றில் அதிகம் வந்தவை",
            note="பிரபலம் என்பது கலாச்சாரமும் பழக்கமும், வெல்லும் வாய்ப்பு அல்ல. 0000 முதல் 9999 வரை ஒவ்வொரு எண்ணுக்கும் ஒவ்வொரு குலுக்கலிலும் சமமான வாய்ப்பு; பலர் வாங்கும் எண் வென்றால் பரிசு பலருக்குப் பிரிக்கப்படும். 21+ · முஸ்லிம் அல்லாதவர்கள் மட்டும் · பொறுப்புடன் விளையாடுங்கள்.",
            cta="எந்த எண்ணையும் சரிபாருங்கள்", stats="முழு 4D புள்ளிவிவரம்"),
}

CSS = """.pop{--mu:#9DB0D3;--cd:#0F1F3D;--ln:#1D3157;--gold:#E9C46B;--ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei","Noto Sans Tamil",sans-serif;font-family:var(--ui)}
.pop h1{font-size:26px;line-height:1.2;letter-spacing:-.4px;margin:6px 0 6px}
.pop .lead{color:var(--mu);margin:0 0 16px;font-size:14px;line-height:1.55;max-width:34em}
.pop .lng{display:flex;gap:6px;margin:4px 0 12px}
.pop .lng a{padding:6px 11px;border-radius:999px;border:1px solid var(--ln);text-decoration:none;font-size:12.5px;font-weight:700;color:#C9D4EA}
.pop .lng a[aria-current]{background:#F8F4E8;color:#07142B;border-color:#F8F4E8}
.pop .tabs{display:flex;gap:6px;overflow-x:auto;margin:14px 0 4px;padding:6px 0;scrollbar-width:none;position:sticky;top:0;z-index:2;background:#07142B}
.pop .tabs::-webkit-scrollbar{display:none}
.pop .tabs a{flex:none;padding:8px 13px;border-radius:999px;border:1px solid #233862;background:var(--cd);font-size:12.5px;font-weight:700;color:#C9D4EA;text-decoration:none}
.pop section{margin-top:24px;scroll-margin-top:70px}
.pop h2{display:flex;align-items:center;gap:9px;font-size:16px;font-weight:700;letter-spacing:-.2px;margin:0 0 10px}
.pop h2 i{font-style:normal;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:rgba(233,196,107,.14);font-size:14px}
.pop .cards{display:grid;gap:8px}
.pop .cards a{display:grid;grid-template-columns:66px minmax(0,1fr) auto;column-gap:13px;row-gap:3px;align-items:center;padding:13px 14px;border-radius:14px;background:var(--cd);border:1px solid #233862;text-decoration:none}
.pop .nm{grid-row:1/3;display:grid;place-items:center;height:50px;border-radius:12px;background:rgba(233,196,107,.13);border:1px solid rgba(233,196,107,.36);font:700 21px/1 var(--ui);font-variant-numeric:tabular-nums;color:#FFE7A3;letter-spacing:.06em}
.pop .nm.hot{background:rgba(255,90,95,.17);border-color:rgba(255,120,110,.5)}
.pop .why{min-width:0;font-size:14.5px;font-weight:500;color:#EDF1F8;line-height:1.4;align-self:end}
.pop .dict{min-width:0;font-size:12.5px;color:var(--mu);line-height:1.35;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;align-self:start}
.pop .ct{align-self:end;text-align:right;white-space:nowrap;font:700 14px/1 var(--ui);font-variant-numeric:tabular-nums;color:#F8F4E8}
.pop .dt{align-self:start;text-align:right;white-space:nowrap;font-size:11.5px;color:#6F80A3;font-variant-numeric:tabular-nums}
.pop .nt{margin-top:24px;padding:14px 16px;border-radius:14px;background:rgba(255,90,95,.08);border:1px solid rgba(255,90,95,.3);font-size:13px;color:#C2CEE4;line-height:1.6}
.pop .cta{display:flex;justify-content:center;align-items:center;height:50px;margin-top:16px;border-radius:999px;background:var(--gold);color:#1A1405;font-weight:700;font-size:15px;text-decoration:none}
.pop .cta2{display:flex;justify-content:center;align-items:center;height:48px;margin-top:8px;border-radius:999px;border:1px solid rgba(233,196,107,.4);color:var(--gold);font-weight:700;text-decoration:none;font-size:14px}
"""


def build(site) -> None:
    import datetime as dt
    d8 = lambda d: dt.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    MON = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
           "ms": ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"],
           "ta": ["ஜன", "பிப்", "மார்", "ஏப்", "மே", "ஜூன்", "ஜூலை", "ஆக", "செப்", "அக்", "நவ", "டிச"]}
    hits = site.hits
    nums = [n for _, _, lst in G for n, _ in lst]
    cnt = {n: len(hits.get(n, [])) for n in nums}
    lastw = {n: max((h[0] for h in hits.get(n, [])), default=None) for n in nums}
    best = max(cnt, key=lambda n: cnt[n])
    s0, s1 = site.dates[0], site.dates[-1]
    import hashlib
    css_name = "assets/pp." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / "assets").mkdir(exist_ok=True)
    (site.out / css_name).write_text(CSS)
    path = lambda l: LANGS[l][1] + "popular-4d-numbers/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}popular-4d-numbers/">'
    names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
    for lang, x in T.items():
        hl, pre = LANGS[lang]
        fm = (lambda d: f"{d.year}年{d.month}月") if lang == "zh" else (lambda d: f"{MON[lang][d.month - 1]} {d.year}")
        fd = (lambda d: f"{d.year}年{d.month}月{d.day}日") if lang == "zh" else (lambda d: f"{d.day} {MON[lang][d.month - 1]} {d.year}")
        fs = (lambda d: f"{d.month}/{d.year % 100}") if lang == "zh" else (lambda d: f"{MON['en' if lang == 'ta' else lang][d.month - 1]} {d.year % 100}")
        S = fm(d8(s0))
        mk = lambda n: site.dict.get(n, {}).get("zh" if lang == "zh" else lang if lang in ("ms", "ta") else "en", "") or site.dict.get(n, {}).get("en", "")
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        tabs = '<nav class="tabs">' + "".join(f'<a href="#{k}">{ic} {esc(x["g"][k])}</a>' for k, ic, _ in G) + "</nav>"
        secs = ""
        for k, ic, lst in G:
            cards = ""
            for n, why in lst:
                c = cnt[n]
                badge = x["won"].format(n=c) if c else x["never"]
                sub = esc(mk(n))
                extra = fs(d8(lastw[n])) if lastw[n] else ""
                cards += (f'<a href="{site.u("4d/" + n + "/")}"><span class="nm{" hot" if n == best else ""}">{n}</span>'
                          f'<span class="why">{esc(why[lang])}</span><span class="ct">{esc(badge)}</span>'
                          f'<span class="dict">{sub or "—"}</span><span class="dt">{esc(extra)}</span></a>')
            secs += f'<section id="{k}"><h2><i>{ic}</i>{esc(x["g"][k])}</h2><div class="cards">{cards}</div></section>'
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        body = (f'<div class="pop">{lng}{bc}<h1>{esc(x["h1"])}</h1>'
                f'<p class="lead">{esc(x["lead"].format(n=f"{site.ndraws:,}", s=S))}</p>{tabs}{secs}'
                f'<div class="nt">{esc(x["note"])}</div>'
                f'<a class="cta" href="{site.u(pre + "?tab=check")}">{esc(x["cta"])} ›</a>'
                f'<a class="cta2" href="{site.u(pre + "4d-statistics/")}">{esc(x["stats"])} ›</a></div>')
        il = {"@context": "https://schema.org", "@type": "ItemList", "name": x["title"], "inLanguage": hl,
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": site.site + f"4d/{n}/"} for i, n in enumerate(nums)]}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"].format(s=S), body, lang=hl, ld=[bld, il],
                  head=f'<link rel="stylesheet" href="{site.u(css_name)}">' + alts, lastmod=d8(s1).isoformat())
