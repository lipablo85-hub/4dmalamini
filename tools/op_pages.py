"""One results page per company, per language, rebuilt every draw:
/magnum-4d-result/, /da-ma-cai-result/, /sports-toto-result/, /gd-lotto-result/, /9-lotto-result/ (+ /ms/ /zh/ /ta/).
Targets searches such as "Magnum 4D result today", "keputusan Magnum 4D hari ini", "今日万能成绩"."""
import datetime as dt
import json
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
# slug, keys on the page, display names per language, colour, draw days text key
CO = [
    ("magnum-4d-result", ["M"], {"en": "Magnum 4D", "ms": "Magnum 4D", "zh": "万能", "ta": "Magnum 4D"}, "#E9C46B", "wss"),
    ("da-ma-cai-result", ["D"], {"en": "Da Ma Cai 1+3D", "ms": "Da Ma Cai 1+3D", "zh": "大马彩", "ta": "Da Ma Cai 1+3D"}, "#4C8DFF", "wss"),
    ("sports-toto-result", ["T"], {"en": "Sports Toto 4D", "ms": "Sports Toto 4D", "zh": "多多", "ta": "Sports Toto 4D"}, "#FF5A5F", "wss"),
    ("gd-lotto-result", ["G"], {"en": "GD Lotto 4D", "ms": "GD Lotto 4D", "zh": "豪龙", "ta": "GD Lotto 4D"}, "#F27BA5", "daily"),
    ("singapore-4d-result", ["S"], {"en": "Singapore 4D", "ms": "Singapore 4D", "zh": "新加坡万字", "ta": "Singapore 4D"}, "#38BDF8", "sg"),
    ("cash-sweep-result", ["C"], {"en": "Sarawak Cash Sweep", "ms": "Sarawak Cash Sweep", "zh": "砂拉越大万", "ta": "Sarawak Cash Sweep"}, "#4ADE80", "wss"),
    ("sabah-88-4d-result", ["B"], {"en": "Sabah 88 4D", "ms": "Sabah 88 4D", "zh": "沙巴88", "ta": "Sabah 88 4D"}, "#E5484D", "wss"),
    ("sandakan-4d-result", ["H"], {"en": "Sandakan STC 4D", "ms": "Sandakan STC 4D", "zh": "山打根万字", "ta": "Sandakan STC 4D"}, "#FACC15", "wss"),
    ("super-j3-j9-result", ["K", "J"], {"en": "Super J3 & J9", "ms": "Super J3 & J9", "zh": "Super J3 & J9", "ta": "Super J3 & J9"}, "#A78BFA", "twice"),
    ("9-lotto-result", ["N"], {"en": "9 Lotto 4D", "ms": "9 Lotto 4D", "zh": "9 Lotto", "ta": "9 Lotto 4D"}, "#2EC4B6", "daily"),
]
MON = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
       "ms": ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"]}
DAY = {"en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
       "ms": ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"],
       "zh": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
       "ta": ["திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி", "ஞாயிறு"]}
T = {
 "en": dict(h1="{n} Result Today", title="{n} Result Today – {d} | 4D Malam Ini", home="Home", crumb="{n} results",
   desc="{n} result for {d}: 1st {a}, 2nd {b}, 3rd {c}. Full Special and Consolation numbers, last 10 draws and draw times. Live from 7pm.",
   latest="Latest {n} result", draw="Draw", p=("1st Prize", "2nd Prize", "3rd Prize", "Special", "Consolation"),
   lead="The {n} result for {day} {d} (draw {no}): 1st prize {a}, 2nd prize {b} and 3rd prize {c}. {sched} On draw nights this page and the live board update as soon as the numbers are out.",
   sched={"wss": "{n} draws every Wednesday, Saturday and Sunday at 7pm Malaysia time, plus special draws announced in advance (usually on a Tuesday).",
          "sg": "{n} (Singapore Pools) draws every Wednesday, Saturday and Sunday at 6:30pm (same time in Singapore and Malaysia).", "daily": "{n} draws every day at 7pm Malaysia time.", "twice": "{n} draws twice every day, at 3pm (J3) and 9pm (J9) Malaysia time."},
   live="Watch tonight's draw live ›", prev="Previous {n} results", date="Date", top="1st · 2nd · 3rd", faqh="{n} result: questions",
   faq=[("What time is the {n} result out?", "{when} Numbers appear on 4D Malam Ini's live board as they are drawn, and the full result is complete within minutes."),
        ("Has my number won {n} before?", "Type your 4-digit number into Check number on 4D Malam Ini to see every win since November 2021, with company, prize and date."),
        ("Is this the official {n} result?", "4D Malam Ini is an independent results site. Results are compiled from what the company publishes and cross-checked; always confirm with {n} before claiming a prize.")],
   when={"wss": "{n} results are drawn at 7pm on Wednesday, Saturday and Sunday (and on announced special draw days).", "sg": "{n} is drawn at 6:30pm every Wednesday, Saturday and Sunday.", "daily": "{n} results are drawn every evening at 7pm.",
         "twice": "{n} draws twice a day: J3 from 3pm and J9 from 9pm."},
   more="More: all companies today ›", archive="Results archive ›", howto="How to play ›", t9=("J3 · 3pm", "J9 · 9pm")),
 "ms": dict(h1="Keputusan {n} Hari Ini", title="Keputusan {n} Hari Ini – {d} | 4D Malam Ini", home="Utama", crumb="Keputusan {n}",
   desc="Keputusan {n} {d}: Pertama {a}, Kedua {b}, Ketiga {c}. Istimewa dan Saguhati penuh, 10 cabutan lepas. Langsung dari 7 malam.",
   latest="Keputusan {n} terkini", draw="Cabutan", p=("Hadiah Pertama", "Hadiah Kedua", "Hadiah Ketiga", "Istimewa", "Saguhati"),
   lead="Keputusan {n} untuk {day}, {d} (cabutan {no}): hadiah pertama {a}, kedua {b} dan ketiga {c}. {sched} Pada malam cabutan, halaman ini dan papan langsung dikemas kini sebaik nombor keluar.",
   sched={"wss": "{n} membuat cabutan setiap Rabu, Sabtu dan Ahad pada 7 malam waktu Malaysia, serta cabutan khas yang diumumkan lebih awal (biasanya hari Selasa).",
          "sg": "{n} (Singapore Pools) membuat cabutan setiap Rabu, Sabtu dan Ahad pada 6:30 petang (waktu sama di Singapura dan Malaysia).", "daily": "{n} membuat cabutan setiap hari pada 7 malam waktu Malaysia.", "twice": "{n} membuat cabutan dua kali setiap hari, pada 3 petang (J3) dan 9 malam (J9) waktu Malaysia."},
   live="Tonton cabutan malam ini secara langsung ›", prev="Keputusan {n} sebelum ini", date="Tarikh", top="Pertama · Kedua · Ketiga", faqh="Keputusan {n}: soalan lazim",
   faq=[("Pukul berapa keputusan {n} keluar?", "{when} Nombor muncul di papan langsung 4D Malam Ini semasa dicabut, dan keputusan penuh lengkap dalam beberapa minit."),
        ("Adakah nombor saya pernah menang {n}?", "Taip nombor 4 digit anda di Semak nombor 4D Malam Ini untuk melihat setiap kemenangan sejak November 2021, dengan syarikat, hadiah dan tarikh."),
        ("Adakah ini keputusan rasmi {n}?", "4D Malam Ini ialah laman keputusan bebas. Keputusan disusun daripada yang diterbitkan syarikat dan disemak silang; sentiasa sahkan dengan {n} sebelum menuntut hadiah.")],
   when={"wss": "Keputusan {n} dicabut pada 7 malam setiap Rabu, Sabtu dan Ahad (dan hari cabutan khas).", "sg": "{n} dicabut pada 6:30 petang setiap Rabu, Sabtu dan Ahad.", "daily": "Keputusan {n} dicabut setiap petang pada 7 malam.",
         "twice": "{n} membuat cabutan dua kali sehari: J3 dari 3 petang dan J9 dari 9 malam."},
   more="Semua syarikat hari ini ›", archive="Arkib keputusan ›", howto="Cara main ›", t9=("J3 · 3 ptg", "J9 · 9 mlm")),
 "zh": dict(h1="今日{n}万字成绩", title="今日{n}万字成绩 – {d} | 4D Malam Ini", home="首页", crumb="{n}成绩",
   desc="{n}万字成绩 {d}：头奖 {a}，二奖 {b}，三奖 {c}。完整特别奖与安慰奖、最近10期成绩与开彩时间。晚上7点起直播。",
   latest="{n}最新成绩", draw="期数", p=("头奖", "二奖", "三奖", "特别奖", "安慰奖"),
   lead="{n} {d}（{day}，第 {no} 期）成绩：头奖 {a}，二奖 {b}，三奖 {c}。{sched}开彩夜号码一开出，本页与直播成绩板即刻更新。",
   sched={"wss": "{n}每逢星期三、六、日晚上7点（马来西亚时间）开彩，另有提前公布的特别开彩（通常在星期二）。", "sg": "{n}（新加坡博彩公司）逢星期三、六、日傍晚6点30分开彩（新马同一时间）。", "daily": "{n}每天晚上7点（马来西亚时间）开彩。",
          "twice": "{n}每天开彩两次：下午3点（J3）和晚上9点（J9），马来西亚时间。"},
   live="观看今晚直播开彩 ›", prev="{n}往期成绩", date="日期", top="头奖 · 二奖 · 三奖", faqh="{n}成绩：常见问题",
   faq=[("{n}成绩几点开出？", "{when}号码开出时会即时显示在 4D Malam Ini 的直播成绩板，几分钟内完整成绩就会出齐。"),
        ("我的号码中过{n}吗？", "在 4D Malam Ini 的「查号码」输入4位号码，即可查看2021年11月以来的每次中奖：公司、奖项与日期。"),
        ("这是{n}的官方成绩吗？", "4D Malam Ini 是独立成绩网站。成绩整理自公司公布的结果并经交叉核对；兑奖前请向{n}确认。")],
   when={"wss": "{n}在星期三、六、日（及特别开彩日）晚上7点开彩。", "sg": "{n}逢星期三、六、日傍晚6点30分开彩。", "daily": "{n}每天晚上7点开彩。", "twice": "{n}每天开彩两次：J3 下午3点起，J9 晚上9点起。"},
   more="今日所有公司成绩 ›", archive="往期成绩 ›", howto="玩法 ›", t9=("J3 · 下午3点", "J9 · 晚上9点")),
 "ta": dict(h1="இன்றைய {n} முடிவுகள்", title="இன்றைய {n} முடிவுகள் – {d} | 4D Malam Ini", home="முகப்பு", crumb="{n} முடிவுகள்",
   desc="{n} முடிவுகள் {d}: முதல் {a}, இரண்டாம் {b}, மூன்றாம் {c}. சிறப்பு & ஆறுதல் எண்கள், கடைசி 10 குலுக்கல். இரவு 7 முதல் நேரலை.",
   latest="சமீபத்திய {n} முடிவு", draw="குலுக்கல்", p=("முதல் பரிசு", "இரண்டாம் பரிசு", "மூன்றாம் பரிசு", "சிறப்பு", "ஆறுதல்"),
   lead="{day}, {d} (குலுக்கல் {no}) {n} முடிவு: முதல் பரிசு {a}, இரண்டாம் {b}, மூன்றாம் {c}. {sched} குலுக்கல் இரவுகளில் எண்கள் வந்தவுடன் இந்தப் பக்கமும் நேரலைப் பலகையும் புதுப்பிக்கப்படும்.",
   sched={"wss": "{n} ஒவ்வொரு புதன், சனி, ஞாயிறு இரவு 7 மணிக்கு (மலேசிய நேரம்) குலுக்கல் நடத்துகிறது; முன்கூட்டியே அறிவிக்கப்படும் சிறப்பு குலுக்கல்களும் உண்டு.",
          "sg": "{n} (Singapore Pools) ஒவ்வொரு புதன், சனி, ஞாயிறு மாலை 6:30 மணிக்கு குலுக்கல் நடத்துகிறது (சிங்கப்பூர், மலேசியா ஒரே நேரம்).", "daily": "{n} தினமும் இரவு 7 மணிக்கு (மலேசிய நேரம்) குலுக்கல் நடத்துகிறது.", "twice": "{n} தினமும் இரண்டு முறை, மதியம் 3 (J3) மற்றும் இரவு 9 (J9) மணிக்கு குலுக்கல் நடத்துகிறது."},
   live="இன்றிரவு குலுக்கலை நேரலையில் பாருங்கள் ›", prev="முந்தைய {n} முடிவுகள்", date="தேதி", top="1 · 2 · 3", faqh="{n} முடிவு: கேள்விகள்",
   faq=[("{n} முடிவு எத்தனை மணிக்கு வரும்?", "{when} எண்கள் குலுக்கப்படும்போதே 4D Malam Ini நேரலைப் பலகையில் தோன்றும்; சில நிமிடங்களில் முழு முடிவு கிடைக்கும்."),
        ("என் எண் முன்பு {n}-இல் வென்றதா?", "4D Malam Ini-இல் எண் சரிபார்ப்பில் உங்கள் 4 இலக்க எண்ணை உள்ளிட்டு, நவம்பர் 2021 முதல் ஒவ்வொரு வெற்றியையும் பாருங்கள்."),
        ("இது அதிகாரப்பூர்வ {n} முடிவா?", "4D Malam Ini ஒரு சுயாதீன முடிவுத் தளம். நிறுவனம் வெளியிடுவதிலிருந்து தொகுத்து சரிபார்க்கப்படுகிறது; பரிசு கோருவதற்கு முன் {n}-இடம் உறுதிசெய்யுங்கள்.")],
   when={"wss": "{n} முடிவுகள் புதன், சனி, ஞாயிறு இரவு 7 மணிக்கு வெளியாகும்.", "sg": "{n} புதன், சனி, ஞாயிறு மாலை 6:30 மணிக்கு குலுக்கப்படும்.", "daily": "{n} முடிவுகள் தினமும் இரவு 7 மணிக்கு வெளியாகும்.",
         "twice": "{n} தினமும் இரண்டு முறை: J3 மதியம் 3 முதல், J9 இரவு 9 முதல்."},
   more="இன்று அனைத்து நிறுவனங்களும் ›", archive="முடிவுக் காப்பகம் ›", howto="விளையாடும் முறை ›", t9=("J3 · மதியம் 3", "J9 · இரவு 9")),
}
GUIDE = {"M": "magnum-4d/", "D": "da-ma-cai-1-3d/", "T": "sports-toto-4d/"}
CSS = """.chips.yr{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}.chips.yr a{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 14px;border-radius:12px;background:#0F1F3D;border:1px solid #233862;text-decoration:none;color:#F8F4E8;font-weight:700}.chips.yr a small{color:#9FB0D3;font-weight:600;font-size:11.5px}
.opp .lead{color:#C9D3EA;line-height:1.65}.opp .card.op{border-left:4px solid var(--c)}.opp .cta{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.opp .cta a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:12px;background:#172A4D;color:#F8F4E8;text-decoration:none;font-weight:700}.opp .cta a.p{background:#E9C46B;color:#1B1300}
.opp table{width:100%;border-collapse:collapse;font-size:14px}.opp td,.opp th{padding:9px 6px;border-bottom:1px solid #1A2C50;text-align:left}.opp th{color:#A9B4CC;font-size:12px}
.opp td.n{font-family:ui-monospace,Menlo,monospace;font-weight:700;letter-spacing:.04em}.opp details{border-bottom:1px solid #1A2C50;padding:12px 0}.opp summary{font-weight:700;cursor:pointer}.opp details p{color:#C9D3EA;margin:8px 0 0}"""


# ---- provider-year archive strings ----
YT = {
 "en": {"h1": "{n} Results {y}", "ttl": "{n} Results {y} — Full Year Archive | 4D Malam Ini",
        "dsc": "Every {n} result in {y}: {c} draws from {a} to {b}. First, second and third prize for each draw date.",
        "lead": "{c} {n} draw dates in {y}, {a} – {b}. Tap a date for the full result including special and consolation prizes.",
        "yrs": "Other years", "all": "All {n} results ›", "mon": "{m} {y}"},
 "ms": {"h1": "Keputusan {n} {y}", "ttl": "Keputusan {n} {y} — Arkib Penuh Setahun | 4D Malam Ini",
        "dsc": "Semua keputusan 4D {n} tahun {y}: {c} cabutan dari {a} hingga {b}. Hadiah pertama, kedua dan ketiga setiap tarikh.",
        "lead": "{c} tarikh cabutan {n} dalam {y}, {a} – {b}. Tekan tarikh untuk keputusan penuh termasuk hadiah istimewa dan saguhati.",
        "yrs": "Tahun lain", "all": "Semua keputusan {n} ›", "mon": "{m} {y}"},
 "zh": {"h1": "{y}年{n}开奖记录", "ttl": "{y}年{n}开奖记录 — 全年万字成绩档案 | 4D Malam Ini",
        "dsc": "{y}年{n}全部开奖记录：{c} 期，{a} 至 {b}。每期头奖、二奖、三奖。",
        "lead": "{y}年{n}共 {c} 期开奖，{a} – {b}。点击日期查看完整成绩，包括特别奖和安慰奖。",
        "yrs": "其他年份", "all": "全部{n}成绩 ›", "mon": "{y}年{m}"},
 "ta": {"h1": "{n} {y} முடிவுகள்", "ttl": "{n} {y} முடிவுகள் — முழு ஆண்டு காப்பகம் | 4D Malam Ini",
        "dsc": "{y} ஆம் ஆண்டின் அனைத்து {n} 4D முடிவுகள்: {a} முதல் {b} வரை {c} குலுக்கல். ஒவ்வொரு தேதிக்கும் முதல், இரண்டாம், மூன்றாம் பரிசு.",
        "lead": "{y} இல் {c} {n} குலுக்கல் தேதிகள், {a} – {b}. முழு முடிவுக்கு தேதியை தட்டவும்.",
        "yrs": "மற்ற ஆண்டுகள்", "all": "அனைத்து {n} முடிவுகள் ›", "mon": "{m} {y}"},
}
ZHMON = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]


def build(site) -> None:
    from seo_pages import d8
    # 1.1 KB — inlined instead of a second stylesheet request on 248 pages
    head0 = "<style>" + CSS + "</style>"

    def fd(d, lang):
        x = d8(d)
        if lang == "zh":
            return f"{x.year}年{x.month}月{x.day}日"
        if lang == "ta":
            return f"{x.day} {MON['en'][x.month - 1]} {x.year}"
        return f"{x.day} {MON['ms' if lang == 'ms' else 'en'][x.month - 1]} {x.year}"

    def card(k, r, lang, x, label=""):
        d, no, n = r
        a = lambda v: f'<a href="{site.u(f"4d/{v}/")}" class="mono">{v}</a>'
        top = "".join(f'<a href="{site.u(f"4d/{v}/")}"><span class="mono">{v}</span><small>{x["p"][j]}</small></a>' for j, v in enumerate(n[:3]))
        return (f'<section class="card op" style="--c:inherit"><h2 style="margin:0">{esc(label or x["latest"])} <small style="color:#A9B4CC;font-weight:600">'
                f'{DAY[lang][d8(d).weekday()]}, {fd(d, lang)}' + (f' · {x["draw"]} {esc(no)}' if no else '') + '</small></h2>'
                f'<div class="top3">{top}</div><div class="lbl">{x["p"][3]}</div><div class="g5">{"".join(a(v) for v in sorted(n[3:13]))}</div>'
                f'<div class="lbl">{x["p"][4]}</div><div class="g5">{"".join(a(v) for v in sorted(n[13:]))}</div>'
                + (f'<div class="lbl">6D Jackpot</div><p class="mono" style="font-size:26px;font-weight:800;letter-spacing:.14em;margin:4px 0 0;color:#E9C46B">{"".join(v[2:] for v in n[:3])}</p>' if k in "JK" else "")
                + '</section>')

    for slug, keys, names, col, sk in CO:
        rows = {k: site.draws.get(k, []) for k in keys}
        if not any(rows.values()):
            continue
        for lang, (hl, pre) in LANGS.items():
            x, nm = T[lang], names[lang]
            f = lambda s, **kw: s.replace("{n}", nm).format(**kw) if kw else s.replace("{n}", nm)
            # newest draw across the page's keys (9 Lotto: 9pm and 7pm)
            lk = max((k for k in keys if rows[k]), key=lambda k: (rows[k][-1][0], k == "K"))
            latest = rows[lk][-1]
            d, no, n = latest
            path = f"{pre}{slug}/"
            sched = f(x["sched"][sk])
            multi = len(keys) > 1
            lab9 = lambda k: x["t9"][1 if k == "K" else 0]
            cards = card(lk, latest, lang, x, (x["latest"].replace("{n}", nm) + (f" · {lab9(lk)}" if multi else "")))
            if multi:
                for k in [k for k in keys if k != lk and rows[k]]:
                    cards += card(k, rows[k][-1], lang, x, f"{nm} · {lab9(k)}")
            hist = sorted((r + (k,) for k in keys for r in rows[k][-10:]), key=lambda r: (r[0], r[3] == "K"), reverse=True)[:10]
            trs = "".join(f'<tr><td><a href="{site.u(f"keputusan/{d8(r[0]).isoformat()}/")}">{fd(r[0], lang)}</a>'
                          + (f' <small style="color:#A9B4CC">{x["t9"][1 if r[3] == "K" else 0]}</small>' if len(keys) > 1 else "")
                          + f'</td><td>{esc(r[1])}</td><td class="n">{" · ".join(r[2][:3])}</td></tr>' for r in hist)
            yrs = {}
            for k in keys:
                for r in rows[k]:
                    yrs.setdefault(r[0][:4], []).append(r + (k,))
            ylist = sorted(yrs, reverse=True)
            y_ = YT[lang]
            ychips = "".join(f'<a href="{site.u(f"{pre}{slug}/{yy}/")}">{yy}<small>{len(yrs[yy])}</small></a>' for yy in ylist)
            faq = [(f(q), f(a_).replace("{when}", f(x["when"][sk])) if "{when}" in a_ else f(a_)) for q, a_ in x["faq"]]
            faq = [(q, a_.replace("{when}", f(x["when"][sk]))) for q, a_ in faq]
            home = site.u(pre)
            links = [f'<a class="p" href="{home}#rc-{lk}">{x["live"]}</a>', f'<a href="{home}">{x["more"]}</a>', f'<a href="{site.u("keputusan/")}">{x["archive"]}</a>']
            if lk in GUIDE:
                links.append(f'<a href="{site.u(pre + "guide/" + GUIDE[lk])}">{x["howto"]}</a>')
            nav, bld = site.crumbs([(x["home"], pre), (f(x["crumb"]), None)])
            lead = (x["lead"] if no else x["lead"].replace(" (draw {no})", "").replace(" (cabutan {no})", "").replace("，第 {no} 期", "").replace(" (குலுக்கல் {no})", "")).replace("{n}", nm).replace("{sched}", sched).format(day=DAY[lang][d8(d).weekday()], d=fd(d, lang), no=no, a=n[0], b=n[1], c=n[2])
            body = (f'<div class="opp" style="--c:{col}">{nav}<h1>{esc(f(x["h1"]))}<small>{DAY[lang][d8(d).weekday()]}, {fd(d, lang)}{(" · " + x["draw"] + " " + esc(no)) if no else ""}</small></h1>'
                    f'<p class="lead">{esc(lead)}</p><div class="cta">{links[0]}</div>{cards}<div class="cta">{"".join(links[1:])}</div>'
                    f'<h2>{esc(f(x["prev"]))}</h2><table><tr><th>{x["date"]}</th><th>{x["draw"]}</th><th>{x["top"]}</th></tr>{trs}</table>'
                    f'<h2>{esc(y_["yrs"])}</h2><div class="chips yr">{ychips}</div>'
                    f'<h2>{esc(f(x["faqh"]))}</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a_)}</p></details>" for q, a_ in faq) + "</div>")
            fql = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a_}} for q, a_ in faq]}
            alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{LANGS[l][1]}{slug}/">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}{slug}/">'
            title = f(x["title"]).replace("{d}", fd(d, lang))
            desc = f(x["desc"]).replace("{d}", fd(d, lang)).replace("{a}", n[0]).replace("{b}", n[1]).replace("{c}", n[2])
            ld_d = {"@context": "https://schema.org", "@type": "Dataset", "name": title.split(" | ")[0], "inLanguage": hl,
                    "description": desc, "url": site.site + path, "isAccessibleForFree": True,
                    "license": site.site + "data-policy/", "temporalCoverage": f"{d8(min(r[0] for k in keys for r in rows[k])).isoformat()}/{d8(d).isoformat()}",
                    "creator": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site}}
            site.page(path, title, desc, body, hl, [bld, fql, ld_d], d8(d).isoformat(), head=head0 + alts)

            # ---- provider-year archives: {pre}{slug}/{year}/ ----
            for yy in ylist:
                rs = sorted(yrs[yy], key=lambda r: (r[0], r[3] == "K"))
                g = {}
                for r in rs:
                    g.setdefault(r[0][4:6], []).append(r)
                mn = lambda mm: (y_["mon"].format(m=ZHMON[int(mm) - 1], y=yy) if lang == "zh"
                                 else y_["mon"].format(m=MON["ms" if lang == "ms" else "en"][int(mm) - 1], y=yy))
                secs = "".join(
                    f'<h2>{mn(mm)}</h2><table><tr><th>{x["date"]}</th><th>{x["draw"]}</th><th>{x["top"]}</th></tr>' + "".join(
                        f'<tr><td><a href="{site.u(f"keputusan/{d8(r[0]).isoformat()}/")}">{fd(r[0], lang)}</a>'
                        + (f' <small style="color:#A9B4CC">{x["t9"][1 if r[3] == "K" else 0]}</small>' if multi else "")
                        + f'</td><td>{esc(r[1])}</td><td class="n">{" · ".join(r[2][:3])}</td></tr>' for r in g[mm]) + "</table>"
                    for mm in sorted(g))
                fa, la = fd(rs[0][0], lang), fd(rs[-1][0], lang)
                sub = dict(n=nm, y=yy, c=len(rs), a=fa, b=la)
                ynav, ybld = site.crumbs([(x["home"], pre), (f(x["crumb"]), f"{pre}{slug}/"), (yy, None)])
                yalts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{LANGS[l][1]}{slug}/{yy}/">' for l in LANGS) \
                    + f'<link rel="alternate" hreflang="x-default" href="{site.site}{slug}/{yy}/">'
                ybody = (f'<div class="opp" style="--c:{col}">{ynav}<h1>{esc(y_["h1"].format(**sub))}<small>{fa} – {la}</small></h1>'
                         f'<p class="lead">{esc(y_["lead"].format(**sub))}</p>'
                         f'<h2>{esc(y_["yrs"])}</h2><div class="chips yr">{ychips}</div>'
                         + secs + f'<div class="cta"><a class="p" href="{site.u(f"{pre}{slug}/")}">{esc(y_["all"].format(n=nm))}</a>'
                         f'<a href="{site.u(f"keputusan/{yy}/") if lang == "ms" else site.u("?d=" + d8(rs[-1][0]).strftime("%Y%m%d"))}">{esc(x["archive"])} {yy}</a></div></div>')
                yld = {"@context": "https://schema.org", "@type": "Dataset", "name": y_["h1"].format(**sub), "inLanguage": hl,
                       "description": y_["dsc"].format(**sub), "url": site.site + f"{pre}{slug}/{yy}/", "isAccessibleForFree": True,
                       "license": site.site + "data-policy/", "temporalCoverage": f"{d8(rs[0][0]).isoformat()}/{d8(rs[-1][0]).isoformat()}",
                       "creator": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site}}
                site.page(f"{pre}{slug}/{yy}/", y_["ttl"].format(**sub), y_["dsc"].format(**sub), ybody, hl,
                          [ybld, yld], d8(rs[-1][0]).isoformat(), head=head0 + yalts)
