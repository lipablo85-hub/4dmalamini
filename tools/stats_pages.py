"""4D statistics page: /4d-statistics/ (+ /ms/ /zh/ /ta/). Past-results statistics only, never predictions.
Hot numbers, numbers missing longest, last-90-days hot, top-3 prize regulars, digit-by-position heat map, Box families."""
import datetime as dt
import json
from collections import Counter, defaultdict
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
MON = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
       "ms": ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"],
       "ta": ["ஜன", "பிப்", "மார்", "ஏப்", "மே", "ஜூன்", "ஜூலை", "ஆக", "செப்", "அக்", "நவ", "டிச"]}

T = {
 "en": dict(title="4D Statistics: Hot & Cold Numbers, Digit Frequency", crumb="4D statistics", home="Home",
            desc="Malaysia 4D statistics from {n} draws since {s}: most drawn numbers, numbers missing longest, top-3 prize regulars, digit frequency by position and Box families.",
            h1="4D statistics", lead="What {n} draws across 10 companies since {s} say about every 4D number. Updated after every draw.",
            k=("Draws analysed", "Numbers drawn", "Different numbers", "Never drawn"),
            hot="Most drawn numbers", hots="All prizes, all companies, since {s}.", cold="Missing longest", colds="Numbers that won before but have not appeared for the longest time.",
            rec="Hot in the last 90 days", recs="Most wins since {d}.", top="Top-3 prize regulars", tops="Most times in 1st, 2nd or 3rd prize.",
            dig="Digit frequency by position", digs="How often each digit appears in each of the 4 positions. Darker gold = more often.", pos=("1st digit", "2nd digit", "3rd digit", "4th digit"),
            box="Most frequent Box families", boxs="All arrangements of the same 4 digits counted together.", combos="{n} arrangements",
            times="×", alltime="all-time {n}×", days="{n}d", last="last", never="{n} numbers have never been drawn since {s}.",
            note="These are past results only. Every draw is independent, so past frequency does not make any number more or less likely to win. 21+ · Non-Muslims only · Play responsibly.",
            more="Check any number", pop="Popular 4D numbers"),
 "ms": dict(title="Statistik 4D: Nombor Panas & Sejuk, Kekerapan Digit", crumb="Statistik 4D", home="Utama",
            desc="Statistik 4D Malaysia daripada {n} cabutan sejak {s}: nombor paling kerap, nombor paling lama tidak keluar, hadiah 1–3, kekerapan digit dan keluarga Box.",
            h1="Statistik 4D", lead="Apa yang {n} cabutan dari 10 syarikat sejak {s} tunjukkan tentang setiap nombor 4D. Dikemas kini selepas setiap cabutan.",
            k=("Cabutan dianalisis", "Nombor dicabut", "Nombor berbeza", "Belum pernah keluar"),
            hot="Nombor paling kerap", hots="Semua hadiah, semua syarikat, sejak {s}.", cold="Paling lama tidak keluar", colds="Nombor yang pernah menang tetapi paling lama tidak muncul.",
            rec="Panas dalam 90 hari", recs="Paling banyak menang sejak {d}.", top="Kerap dalam hadiah 1–3", tops="Paling kerap dalam hadiah Pertama, Kedua atau Ketiga.",
            dig="Kekerapan digit mengikut kedudukan", digs="Berapa kerap setiap digit muncul di setiap kedudukan. Emas lebih gelap = lebih kerap.", pos=("Digit 1", "Digit 2", "Digit 3", "Digit 4"),
            box="Keluarga Box paling kerap", boxs="Semua susunan 4 digit yang sama dikira bersama.", combos="{n} susunan",
            times="×", alltime="jumlah {n}×", days="{n}h", last="terakhir", never="{n} nombor belum pernah keluar sejak {s}.",
            note="Ini hanya keputusan lepas. Setiap cabutan adalah bebas, jadi kekerapan lepas tidak menjadikan mana-mana nombor lebih atau kurang berpeluang. 21+ · Bukan Islam sahaja · Main secara bertanggungjawab.",
            more="Semak mana-mana nombor", pop="Nombor 4D popular"),
 "zh": dict(title="万字统计：热门与冷门号码、数字出现频率", crumb="万字统计", home="首页",
            desc="根据{s}以来{n}期马来西亚万字开彩统计：最常开出号码、最久未开号码、前三奖常客、各位数字频率与 Box 号码组。",
            h1="万字统计", lead="{s}以来10家公司共{n}期开彩，每个万字号码的出现记录。每期开彩后更新。",
            k=("统计期数", "开出号码", "不同号码", "从未开出"),
            hot="最常开出的号码", hots="所有奖项、所有公司，{s}至今。", cold="最久未开的号码", colds="曾经中过、但已经最久没有再出现的号码。",
            rec="近90天热门", recs="{d}以来中奖最多。", top="前三奖常客", tops="最常进入头奖、二奖或三奖。",
            dig="各位数字出现频率", digs="每个数字在4个位置出现的次数，金色越深越常出现。", pos=("第1位", "第2位", "第3位", "第4位"),
            box="最常开出的 Box 号码组", boxs="同样4个数字的所有排列合并计算。", combos="{n} 种排列",
            times="次", alltime="累计 {n} 次", days="{n} 天", last="最近", never="{s}以来有 {n} 个号码从未开出。",
            note="以上只是过往成绩。每期开彩都是独立的，过去出现次数不会让任何号码更容易或更难中奖。仅限21岁或以上非穆斯林 · 理性投注。",
            more="查询任何号码", pop="热门万字号码"),
 "ta": dict(title="4D புள்ளிவிவரம்: அதிகம் & குறைவாக வந்த எண்கள், இலக்க அதிர்வெண்", crumb="4D புள்ளிவிவரம்", home="முகப்பு",
            desc="{s} முதல் {n} குலுக்கல்களின் மலேசியா 4D புள்ளிவிவரம்: அதிகம் வந்த எண்கள், நீண்ட நாள் வராத எண்கள், முதல் 3 பரிசுகள், இலக்க அதிர்வெண், Box குடும்பங்கள்.",
            h1="4D புள்ளிவிவரம்", lead="{s} முதல் 10 நிறுவனங்களின் {n} குலுக்கல்கள் ஒவ்வொரு 4D எண்ணைப் பற்றியும் சொல்வது. ஒவ்வொரு குலுக்கலுக்குப் பின் புதுப்பிக்கப்படும்.",
            k=("ஆய்வு செய்த குலுக்கல்கள்", "வந்த எண்கள்", "வெவ்வேறு எண்கள்", "ஒருமுறையும் வராதவை"),
            hot="அதிகம் வந்த எண்கள்", hots="எல்லா பரிசுகளும், எல்லா நிறுவனங்களும், {s} முதல்.", cold="நீண்ட நாள் வராதவை", colds="முன்பு வென்று, நீண்ட காலமாக மீண்டும் வராத எண்கள்.",
            rec="கடந்த 90 நாளில் அதிகம்", recs="{d} முதல் அதிக வெற்றிகள்.", top="முதல் 3 பரிசில் அடிக்கடி", tops="1வது, 2வது, 3வது பரிசில் அதிக முறை.",
            dig="நிலை வாரியான இலக்க அதிர்வெண்", digs="4 நிலைகளிலும் ஒவ்வொரு இலக்கமும் எத்தனை முறை வருகிறது. அடர் தங்கம் = அதிகம்.", pos=("1வது இலக்கம்", "2வது இலக்கம்", "3வது இலக்கம்", "4வது இலக்கம்"),
            box="அதிகம் வந்த Box குடும்பங்கள்", boxs="அதே 4 இலக்கங்களின் எல்லா வரிசைகளும் சேர்த்து எண்ணப்படுகின்றன.", combos="{n} வரிசைகள்",
            times="×", alltime="மொத்தம் {n}×", days="{n}நா", last="கடைசி", never="{s} முதல் {n} எண்கள் ஒருமுறையும் வரவில்லை.",
            note="இவை கடந்த முடிவுகள் மட்டுமே. ஒவ்வொரு குலுக்கலும் தனித்தது; கடந்த அதிர்வெண் எந்த எண்ணின் வாய்ப்பையும் மாற்றாது. 21+ · முஸ்லிம் அல்லாதவர்கள் மட்டும் · பொறுப்புடன் விளையாடுங்கள்.",
            more="எந்த எண்ணையும் சரிபாருங்கள்", pop="பிரபல 4D எண்கள்"),
}

CSS = """.st4{--mu:#9DB0D3;--cd:#0F1F3D;--ln:#1D3157;--gold:#E9C46B;--ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei","Noto Sans Tamil",sans-serif;font-family:var(--ui)}
.st4 h1{font-size:26px;line-height:1.2;letter-spacing:-.4px;margin:6px 0 6px}
.st4 .lead{color:var(--mu);margin:0 0 16px;font-size:14px;line-height:1.55;max-width:34em}
.st4 .lng{display:flex;gap:6px;margin:4px 0 12px}
.st4 .lng a{padding:6px 11px;border-radius:999px;border:1px solid var(--ln);text-decoration:none;font-size:12.5px;font-weight:700;color:#C9D4EA}
.st4 .lng a[aria-current]{background:#F8F4E8;color:#07142B;border-color:#F8F4E8}
.st4 .kp{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.st4 .kp div:nth-child(3):last-child{grid-column:1/-1}
.st4 .kp div{padding:13px 14px;border-radius:14px;background:var(--cd);border:1px solid #233862}
.st4 .kp b{display:block;font:700 23px/1.15 var(--ui);font-variant-numeric:tabular-nums;color:#FFE7A3;letter-spacing:-.3px}
.st4 .kp small{display:block;margin-top:3px;font-size:12px;color:var(--mu);font-weight:600;line-height:1.3}
.st4 .tabs{display:flex;gap:6px;overflow-x:auto;margin:16px 0 4px;padding:6px 0;scrollbar-width:none;position:sticky;top:0;z-index:2;background:#07142B}
.st4 .tabs::-webkit-scrollbar{display:none}
.st4 .tabs a{flex:none;padding:8px 13px;border-radius:999px;border:1px solid #233862;background:var(--cd);font-size:12.5px;font-weight:700;color:#C9D4EA;text-decoration:none}
.st4 section{margin-top:22px;scroll-margin-top:70px}
.st4 h2{display:flex;align-items:center;gap:9px;font-size:16px;font-weight:700;letter-spacing:-.2px;margin:0 0 3px}
.st4 h2 i{font-style:normal;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:rgba(233,196,107,.14);font-size:14px}
.st4 .sub{color:var(--mu);font-size:12.5px;line-height:1.45;margin:0 0 9px}
.st4 .card{background:var(--cd);border:1px solid #233862;border-radius:16px;padding:4px 14px}
.st4 ol{list-style:none;margin:0;padding:0}
.st4 li{border-bottom:1px solid var(--ln)}.st4 li:last-child{border-bottom:0}
.st4 li a{display:grid;grid-template-columns:22px minmax(0,1fr) auto;column-gap:11px;row-gap:2px;align-items:center;padding:11px 0;text-decoration:none}
.st4 li .r{grid-row:1/3;font-size:11.5px;color:#6F80A3;font-weight:700;text-align:center;font-variant-numeric:tabular-nums}
.st4 li .n{font:700 19px/1.1 var(--ui);font-variant-numeric:tabular-nums;color:#FFE7A3;letter-spacing:.05em;align-self:end}
.st4 li .c{font:700 15px/1.1 var(--ui);font-variant-numeric:tabular-nums;color:#F8F4E8;text-align:right;white-space:nowrap;align-self:end}
.st4 li .m{font-size:12.5px;line-height:1.35;color:var(--mu);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;align-self:start}
.st4 li .d{font-size:11.5px;line-height:1.35;color:#6F80A3;text-align:right;white-space:nowrap;align-self:start;font-variant-numeric:tabular-nums}
.st4 li u{grid-column:2/4;display:block;height:3px;border-radius:2px;background:linear-gradient(90deg,#E9C46B,#F0B98A);text-decoration:none;margin-top:5px}
.st4 li.cold u{background:linear-gradient(90deg,#4C8DFF,#38BDF8)}
.st4 .hm{display:grid;grid-template-columns:58px repeat(10,minmax(0,1fr));gap:3px;font-size:11px}
.st4 .hm b{display:grid;place-items:center;height:20px;color:var(--mu);font-weight:700;font-variant-numeric:tabular-nums}
.st4 .hm span{display:grid;place-items:center;height:32px;border-radius:6px;font-weight:700;color:#1A1405;font-size:10.5px;font-variant-numeric:tabular-nums}
.st4 .hm em{font-style:normal;display:flex;align-items:center;color:#C9D4EA;font-weight:600;font-size:11px}
.st4 .bx{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.st4 .bx a{padding:11px 13px;border-radius:14px;background:var(--cd);border:1px solid #233862;text-decoration:none}
.st4 .bx b{display:block;font:700 18px/1.1 var(--ui);font-variant-numeric:tabular-nums;color:#FFE7A3;letter-spacing:.06em}
.st4 .bx small{display:block;font-size:12px;color:var(--mu);margin-top:4px;line-height:1.3}.st4 .bx strong{color:#F8F4E8;font-weight:700}
.st4 .nt{margin-top:24px;padding:14px 16px;border-radius:14px;background:rgba(255,90,95,.08);border:1px solid rgba(255,90,95,.3);font-size:13px;color:#C2CEE4;line-height:1.6}
.st4 .cta2{display:flex;justify-content:center;align-items:center;height:48px;margin-top:8px;border-radius:999px;border:1px solid rgba(233,196,107,.4);color:var(--gold);font-weight:700;text-decoration:none;font-size:14px}
.st4 .cta{display:flex;justify-content:center;align-items:center;height:50px;margin-top:16px;border-radius:999px;background:var(--gold);color:#1A1405;font-weight:700;font-size:15px;text-decoration:none}
@media (min-width:620px){.st4 .kp{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""


def build(site) -> None:
    hits = site.hits
    dates = site.dates
    s0, s1 = dates[0], dates[-1]
    d8 = lambda d: dt.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    last = d8(s1)
    nd = site.ndraws
    cnt = {n: len(v) for n, v in hits.items() if v}
    total = sum(cnt.values())
    never = 10000 - len(cnt)
    hot = sorted(cnt, key=lambda n: (-cnt[n], -int(max(h[0] for h in hits[n]))))[:15]
    lastwin = {n: max(h[0] for h in hits[n]) for n in cnt}
    cold = sorted(cnt, key=lambda n: (lastwin[n], n))[:15]
    since90 = (last - dt.timedelta(days=90)).strftime("%Y%m%d")
    rc = Counter({n: sum(1 for h in hits[n] if h[0] >= since90) for n in cnt})
    rec = [n for n, c in rc.most_common(15) if c]
    tc = Counter({n: sum(1 for h in hits[n] if h[3] <= 3) for n in cnt})
    top = [n for n, c in tc.most_common(15) if c]
    pos = [[0] * 10 for _ in range(4)]
    for rows in site.draws.values():
        for _, _, nums in rows:
            for v in nums:
                if len(v) == 4 and v.isdigit():
                    for i, ch in enumerate(v):
                        pos[i][int(ch)] += 1
    fam = defaultdict(int)
    for n, c in cnt.items():
        fam["".join(sorted(n))] += c
    from itertools import permutations
    boxes = sorted(fam, key=lambda k: -fam[k])[:12]
    import hashlib
    css_name = "assets/st." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / "assets").mkdir(exist_ok=True)
    (site.out / css_name).write_text(CSS)
    path = lambda l: LANGS[l][1] + "4d-statistics/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}4d-statistics/">'
    names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
    for lang, x in T.items():
        hl, pre = LANGS[lang]
        fd = (lambda d: f"{d.year}年{d.month}月{d.day}日") if lang == "zh" else (lambda d: f"{d.day} {MON[lang][d.month - 1]} {d.year}")
        fm = (lambda d: f"{d.year}年{d.month}月") if lang == "zh" else (lambda d: f"{MON[lang][d.month - 1]} {d.year}")
        S = fm(d8(s0))
        mk = lambda n: site.dict.get(n, {}).get("zh" if lang == "zh" else lang if lang in ("ms", "ta") else "en", "") or site.dict.get(n, {}).get("en", "") or site.dict.get(n, {}).get("zh", "")

        tm = x["times"]

        def rows(ns, val, sub, mx, cls=""):
            return "<ol>" + "".join(
                f'<li class="{cls}"><a href="{site.u("4d/" + n + "/")}"><span class="r">{i + 1}</span><span class="n">{n}</span><span class="c">{val(n)}{tm}</span>'
                f'<span class="m">{esc(mk(n)) or "&nbsp;"}</span><span class="d">{sub(n)}</span>'
                f'<u style="width:{max(6, val(n) / mx * 100):.0f}%"></u></a></li>' for i, n in enumerate(ns)) + "</ol>"
        fs = (lambda d: f"{d.month}/{d.year % 100}") if lang == "zh" else (lambda d: f"{MON['en' if lang == 'ta' else lang][d.month - 1]} {d.year % 100}")
        lw = lambda n: esc(fs(d8(lastwin[n])))
        hot_h = rows(hot, lambda n: cnt[n], lw, cnt[hot[0]])
        cmx = (last - d8(lastwin[cold[0]])).days
        cold_h = "<ol>" + "".join(
            f'<li class="cold"><a href="{site.u("4d/" + n + "/")}"><span class="r">{i + 1}</span><span class="n">{n}</span><span class="c">{esc(x["days"].format(n=(last - d8(lastwin[n])).days))}</span>'
            f'<span class="m">{esc(mk(n)) or "&nbsp;"}</span><span class="d">{esc(fs(d8(lastwin[n])))}</span>'
            f'<u style="width:{max(6, (last - d8(lastwin[n])).days / cmx * 100):.0f}%"></u></a></li>' for i, n in enumerate(cold)) + "</ol>"
        rec_h = rows(rec, lambda n: rc[n], lambda n: esc(x["alltime"].format(n=cnt[n])), rc[rec[0]]) if rec else ""
        top_h = rows(top, lambda n: tc[n], lw, tc[top[0]])
        mxp = max(max(r) for r in pos); mnp = min(min(r) for r in pos)
        hm = '<div class="hm"><b></b>' + "".join(f"<b>{d}</b>" for d in range(10))
        for i in range(4):
            hm += f'<em>{esc(x["pos"][i])}</em>' + "".join(
                f'<span title="{pos[i][d]:,}" style="background:rgba(233,196,107,{0.18 + 0.82 * (pos[i][d] - mnp) / max(1, mxp - mnp):.2f})">{pos[i][d] / sum(pos[i]) * 100:.1f}</span>' for d in range(10))
        hm += "</div>"
        bx = '<div class="bx">' + "".join(
            f'<a href="{site.u("4d/" + k + "/")}"><b>{k}</b><small><strong>{fam[k]}{"次" if lang == "zh" else "×"}</strong> · {esc(x["combos"].format(n=len(set(permutations(k)))))}</small></a>' for k in boxes) + "</div>"
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        vals = [f"{nd:,}", f"{total:,}", f"{len(cnt):,}"] + ([f"{never:,}"] if never else [])
        kp = '<div class="kp">' + "".join(f"<div><b>{v}</b><small>{esc(lb)}</small></div>" for v, lb in zip(vals, x["k"])) + "</div>"
        ids = [("hot", "🔥", x["hot"]), ("cold", "❄️", x["cold"]), ("recent", "📈", x["rec"]), ("top3", "🏆", x["top"]), ("digits", "🔢", x["dig"]), ("box", "🎲", x["box"])]
        tabs = '<nav class="tabs">' + "".join(f'<a href="#{i}">{ic} {esc(t)}</a>' for i, ic, t in ids) + "</nav>"
        sec = lambda i, ic, t, sub, body: f'<section id="{i}"><h2><i>{ic}</i>{esc(t)}</h2><p class="sub">{esc(sub)}</p>{body}</section>'
        body = (f'<div class="st4">{lng}' + site.crumbs([(x["home"], pre), (x["crumb"], None)])[0]
                + f'<h1>{esc(x["h1"])}</h1><p class="lead">{esc(x["lead"].format(n=f"{nd:,}", s=S))}</p>{kp}{tabs}'
                + sec("hot", "🔥", x["hot"], x["hots"].format(s=S), f'<div class="card">{hot_h}</div>')
                + sec("cold", "❄️", x["cold"], x["colds"], f'<div class="card">{cold_h}</div>')
                + sec("recent", "📈", x["rec"], x["recs"].format(d=fd(d8(since90))), f'<div class="card">{rec_h}</div>')
                + sec("top3", "🏆", x["top"], x["tops"], f'<div class="card">{top_h}</div>')
                + sec("digits", "🔢", x["dig"], x["digs"], f'<div class="card" style="padding:12px">{hm}</div>')
                + sec("box", "🎲", x["box"], x["boxs"], bx)
                + (f'<p class="sub" style="margin-top:14px">{esc(x["never"].format(n=f"{never:,}", s=S))}</p>' if never else "")
                + f'<a class="cta" href="{site.u(pre + "?tab=check")}">{esc(x["more"])} ›</a>'
                + f'<a class="cta2" href="{site.u(pre + "popular-4d-numbers/")}">{esc(x["pop"])} ›</a><div class="nt">{esc(x["note"])}</div></div>')
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        ds = {"@context": "https://schema.org", "@type": "Dataset", "name": x["title"], "description": x["desc"].format(n=f"{nd:,}", s=S), "inLanguage": hl,
              "temporalCoverage": f"{d8(s0).isoformat()}/{last.isoformat()}", "creator": {"@type": "Organization", "name": "4D Malam Ini"}}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"].format(n=f"{nd:,}", s=S), body, lang=hl, ld=[bld, ds],
                  head=f'<link rel="stylesheet" href="{site.u(css_name)}">' + alts, lastmod=last.isoformat())
