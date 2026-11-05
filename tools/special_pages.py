"""Special draw page: /special-draw/ (+ /ms/ /zh/ /ta/).
Upcoming special draw with countdown, this year's schedule, and an archive of every past special draw
(dates when Magnum drew outside Wed/Sat/Sun), each linking to that day's results. Dates: tools/special_draws.json."""
import datetime as dt
import json
from html import escape as esc
from pathlib import Path

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
MON = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
       "ms": ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"],
       "ta": ["ஜன", "பிப்", "மார்", "ஏப்", "மே", "ஜூன்", "ஜூலை", "ஆக", "செப்", "அக்", "நவ", "டிச"]}
WD = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "ms": ["Isn", "Sel", "Rab", "Kha", "Jum", "Sab", "Ahd"],
      "zh": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"], "ta": ["தி", "செ", "பு", "வி", "வெ", "ச", "ஞா"]}

T = {
 "en": dict(title="4D Special Draw 2026: Dates, Schedule & Results", crumb="Special draw", home="Home",
            desc="Malaysia 4D special draw dates for 2026 and the next special draw, with results of every past special draw for Magnum, Toto, Da Ma Cai and more.",
            h1="4D special draw dates & results", lead="Extra draws on top of the usual Wednesday, Saturday and Sunday, held by Magnum, Sports Toto, Da Ma Cai, Cash Sweep and Sandakan at 7pm.",
            nx="Next special draw", days="{n} days to go", tom="Tomorrow", today="Today, 7pm", none="The next special draw dates have not been announced yet.",
            sch="{y} special draw schedule", st=("Date", "Day", "Status"), done="Results", up="Upcoming", arch="Past special draws", archs="Tap a date to open that night's full results.",
            m1="Magnum 1st", what="What is a 4D special draw?",
            p=["A special draw is an extra draw approved by the Ministry of Finance, usually on a Tuesday. The five companies draw at the same time as a normal night, 7pm Malaysia time, with the same prizes.",
               "GD Lotto, 9 Lotto and Super J3/J9 already draw every day, and Singapore 4D does not take part in Malaysian special draws.",
               "Dates are added here as soon as they are announced. Always confirm with the operator before buying or claiming."],
            fh="Special draw questions",
            faq=[("When is the next 4D special draw?", "{next}"),
                 ("Which companies hold special draws?", "Magnum 4D, Sports Toto, Da Ma Cai, Cash Sweep (Sarawak) and Sandakan STC 4D. They draw at 7pm Malaysia time."),
                 ("Are special draw prizes different?", "No. Prizes and bet types are the same as a normal draw night. Check each company's official page for jackpot details.")],
            nxs="The next special draw is on {d} at 7pm.", rp="21+ · Non-Muslims only · Play responsibly. 4D Malam Ini does not sell tickets or take bets."),
 "ms": dict(title="Cabutan Khas 4D 2026: Tarikh, Jadual & Keputusan", crumb="Cabutan khas", home="Utama",
            desc="Tarikh cabutan khas 4D Malaysia 2026 dan cabutan khas seterusnya, dengan keputusan setiap cabutan khas lepas untuk Magnum, Toto, Da Ma Cai dan lagi.",
            h1="Tarikh & keputusan cabutan khas 4D", lead="Cabutan tambahan selain Rabu, Sabtu dan Ahad biasa, oleh Magnum, Sports Toto, Da Ma Cai, Cash Sweep dan Sandakan pada 7 malam.",
            nx="Cabutan khas seterusnya", days="{n} hari lagi", tom="Esok", today="Hari ini, 7 mlm", none="Tarikh cabutan khas seterusnya belum diumumkan.",
            sch="Jadual cabutan khas {y}", st=("Tarikh", "Hari", "Status"), done="Keputusan", up="Akan datang", arch="Cabutan khas lepas", archs="Tekan tarikh untuk membuka keputusan penuh malam itu.",
            m1="Magnum Pertama", what="Apa itu cabutan khas 4D?",
            p=["Cabutan khas ialah cabutan tambahan yang diluluskan oleh Kementerian Kewangan, biasanya pada hari Selasa. Lima syarikat membuat cabutan pada masa biasa, 7 malam waktu Malaysia, dengan hadiah yang sama.",
               "GD Lotto, 9 Lotto dan Super J3/J9 sudah membuat cabutan setiap hari, dan Singapore 4D tidak menyertai cabutan khas Malaysia.",
               "Tarikh ditambah di sini sebaik diumumkan. Sentiasa sahkan dengan syarikat sebelum membeli atau menuntut."],
            fh="Soalan cabutan khas",
            faq=[("Bilakah cabutan khas 4D seterusnya?", "{next}"),
                 ("Syarikat mana yang membuat cabutan khas?", "Magnum 4D, Sports Toto, Da Ma Cai, Cash Sweep (Sarawak) dan Sandakan STC 4D, pada 7 malam waktu Malaysia."),
                 ("Adakah hadiah cabutan khas berbeza?", "Tidak. Hadiah dan jenis pertaruhan sama seperti malam cabutan biasa. Semak laman rasmi syarikat untuk butiran jackpot.")],
            nxs="Cabutan khas seterusnya pada {d}, 7 malam.", rp="21+ · Bukan Islam sahaja · Main secara bertanggungjawab. 4D Malam Ini tidak menjual tiket atau menerima pertaruhan."),
 "zh": dict(title="2026万字特别开彩：日期、时间表与成绩", crumb="特别开彩", home="首页",
            desc="2026年马来西亚万字特别开彩日期与下一期特别开彩，附万能、多多、大马彩、砂拉越大万、山打根历年特别开彩成绩。",
            h1="万字特别开彩日期与成绩", lead="在一般星期三、六、日以外的额外开彩，由万能、多多、大马彩、砂拉越大万和山打根在晚上7点开彩。",
            nx="下一期特别开彩", days="还有 {n} 天", tom="明天", today="今天晚上7点", none="下一期特别开彩日期尚未公布。",
            sch="{y}年特别开彩时间表", st=("日期", "星期", "状态"), done="成绩", up="即将开彩", arch="历年特别开彩", archs="点日期即可查看当晚完整成绩。",
            m1="万能头奖", what="什么是万字特别开彩？",
            p=["特别开彩是经财政部批准的额外开彩，通常在星期二。五家公司和平常一样在马来西亚时间晚上7点开彩，奖金相同。",
               "豪龙、9 Lotto 与 Super J3/J9 本来就每天开彩，新加坡万字不参与马来西亚的特别开彩。",
               "日期一公布就会更新在这里。购买或兑奖前请向公司核实。"],
            fh="特别开彩常见问题",
            faq=[("下一期万字特别开彩是哪天？", "{next}"),
                 ("哪些公司有特别开彩？", "万能、多多、大马彩、砂拉越大万和山打根，马来西亚时间晚上7点开彩。"),
                 ("特别开彩的奖金不一样吗？", "一样。奖金和玩法与平常开彩相同，积宝详情请看各公司官网。")],
            nxs="下一期特别开彩：{d} 晚上7点。", rp="21+ · 仅限非穆斯林 · 理性投注。4D Malam Ini 不卖彩票、不接受投注。"),
 "ta": dict(title="4D சிறப்புக் குலுக்கல் 2026: தேதி & முடிவுகள்", crumb="சிறப்புக் குலுக்கல்", home="முகப்பு",
            desc="2026 மலேசியா 4D சிறப்புக் குலுக்கல் தேதிகள், அடுத்த குலுக்கல், Magnum, Sports Toto, Da Ma Cai கடந்த சிறப்புக் குலுக்கல் முடிவுகள்.",
            h1="4D சிறப்புக் குலுக்கல் தேதிகள் & முடிவுகள்", lead="வழக்கமான புதன், சனி, ஞாயிறுக்கு மேலாக Magnum, Sports Toto, Da Ma Cai, Cash Sweep, Sandakan இரவு 7 மணிக்கு நடத்தும் கூடுதல் குலுக்கல்கள்.",
            nx="அடுத்த சிறப்புக் குலுக்கல்", days="இன்னும் {n} நாட்கள்", tom="நாளை", today="இன்று இரவு 7", none="அடுத்த சிறப்புக் குலுக்கல் தேதிகள் இன்னும் அறிவிக்கப்படவில்லை.",
            sch="{y} சிறப்புக் குலுக்கல் அட்டவணை", st=("தேதி", "நாள்", "நிலை"), done="முடிவுகள்", up="வரவிருக்கிறது", arch="கடந்த சிறப்புக் குலுக்கல்கள்", archs="அன்றிரவு முழு முடிவுகளைக் காண தேதியைத் தட்டுங்கள்.",
            m1="Magnum 1வது", what="4D சிறப்புக் குலுக்கல் என்றால் என்ன?",
            p=["சிறப்புக் குலுக்கல் என்பது நிதி அமைச்சு அங்கீகரிக்கும் கூடுதல் குலுக்கல், பொதுவாக செவ்வாய்க்கிழமை. ஐந்து நிறுவனங்களும் வழக்கம் போல் மலேசிய நேரம் இரவு 7 மணிக்கு, அதே பரிசுகளுடன் குலுக்கல் நடத்துகின்றன.",
               "GD Lotto, 9 Lotto, Super J3/J9 ஏற்கனவே தினமும் குலுக்கல் நடத்துகின்றன; Singapore 4D மலேசிய சிறப்புக் குலுக்கல்களில் பங்கேற்பதில்லை.",
               "தேதிகள் அறிவிக்கப்பட்டவுடன் இங்கே சேர்க்கப்படும். வாங்கும் அல்லது பரிசு கோரும் முன் நிறுவனத்திடம் உறுதிப்படுத்துங்கள்."],
            fh="சிறப்புக் குலுக்கல் கேள்விகள்",
            faq=[("அடுத்த 4D சிறப்புக் குலுக்கல் எப்போது?", "{next}"),
                 ("எந்த நிறுவனங்கள் சிறப்புக் குலுக்கல் நடத்துகின்றன?", "Magnum 4D, Sports Toto, Da Ma Cai, Cash Sweep (சரவாக்), Sandakan STC 4D — மலேசிய நேரம் இரவு 7 மணி."),
                 ("சிறப்புக் குலுக்கல் பரிசுகள் வேறுபடுமா?", "இல்லை. பரிசுகளும் பந்தய வகைகளும் வழக்கமான குலுக்கல் போலவே. ஜாக்பாட் விவரங்களுக்கு அதிகாரப்பூர்வ தளத்தைப் பாருங்கள்.")],
            nxs="அடுத்த சிறப்புக் குலுக்கல்: {d}, இரவு 7 மணி.", rp="21+ · முஸ்லிம் அல்லாதவர்கள் மட்டும் · பொறுப்புடன் விளையாடுங்கள். 4D Malam Ini டிக்கெட் விற்பதோ பந்தயம் ஏற்பதோ இல்லை."),
}

CSS = """.sdp{--mu:#9DB0D3;--cd:#0F1F3D;--ln:#1D3157;--gold:#E9C46B}.sdp h1{margin:8px 0 6px}.sdp .lead{color:var(--mu);margin:0 0 16px}
.sdp .lng{display:flex;gap:6px;margin:4px 0 10px}.sdp .lng a{padding:5px 10px;border-radius:999px;border:1px solid var(--ln);text-decoration:none;font-size:13px;font-weight:800;color:#C9D4EA}.sdp .lng a[aria-current]{background:#F8F4E8;color:#07142B}
.sdp .nx{display:flex;align-items:center;gap:14px;padding:16px;border-radius:18px;background:linear-gradient(135deg,rgba(233,196,107,.18),rgba(233,196,107,.05));border:1px solid rgba(233,196,107,.5)}
.sdp .cal{flex:none;width:74px;border-radius:14px;overflow:hidden;text-align:center;background:#fff;color:#1a1a1a}.sdp .cal small{display:block;background:#C00000;color:#fff;font:800 12px/1 Roboto,Arial,sans-serif;padding:5px 0;letter-spacing:.08em}
.sdp .cal b{display:block;font:900 32px/1.1 Roboto,Arial,sans-serif;padding:4px 0 0}.sdp .cal span{display:block;font:700 12px/1 Roboto,Arial,sans-serif;color:#555;padding:2px 0 7px}
.sdp .nx small{display:block;color:var(--mu);font-weight:700;font-size:12.5px}.sdp .nx strong{display:block;font-size:20px;color:#FFE7A3;margin:2px 0}.sdp .nx em{font-style:normal;display:inline-block;margin-top:4px;padding:4px 10px;border-radius:999px;background:var(--gold);color:#1A1405;font-weight:900;font-size:13px}
.sdp .lg{display:flex;gap:4px;margin-top:8px}.sdp .lg i{width:22px;height:22px;border-radius:6px;background:url(/img/op/tk.webp) 0 0/220px 22px no-repeat}
.sdp table{width:100%;border-collapse:collapse;font-size:14px}.sdp th,.sdp td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--ln)}.sdp th{color:var(--mu);font-size:12px}
.sdp .ok{color:#4ADE80;font-weight:800}.sdp .up{color:var(--gold);font-weight:800}.sdp .card{background:var(--cd);border:1px solid #233862;border-radius:18px;padding:6px 12px;margin-top:10px}
.sdp .yr{margin-top:18px}.sdp .yr h3{font-size:15px;margin:0 0 8px;color:#F8F4E8}.sdp .ds{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.sdp .ds a{display:block;padding:10px 12px;border-radius:12px;background:var(--cd);border:1px solid #233862;text-decoration:none}.sdp .ds b{display:block;color:#F8F4E8;font-size:14px}.sdp .ds small{color:var(--mu);font-size:12px}.sdp .ds span{font-family:ui-monospace,Menlo,monospace;color:#FFE7A3;font-weight:800}
.sdp details{background:var(--cd);border:1px solid #233862;border-radius:14px;padding:12px 14px;margin:8px 0}.sdp summary{font-weight:800;cursor:pointer}.sdp .rp{margin-top:20px;padding:12px 14px;border-radius:14px;background:rgba(255,90,95,.08);border:1px solid rgba(255,90,95,.35);font-size:13px}
"""


def build(site) -> None:
    spd = [dt.date.fromisoformat(d) for d in json.loads(Path(__file__).with_name("special_draws.json").read_text())["dates"]]
    m = {r[0]: r for r in site.draws.get("M", [])}
    past = sorted({dt.date(int(d[:4]), int(d[4:6]), int(d[6:])) for d in m} - {x for x in []})
    past = [d for d in past if d.weekday() not in (2, 5, 6)]
    allsp = sorted(set(past) | set(spd))
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()
    nxt = next((d for d in allsp if d >= today and d.strftime("%Y%m%d") not in m), None)
    yr = (nxt or today).year
    import hashlib
    css_name = "assets/sd." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / "assets").mkdir(exist_ok=True)
    (site.out / css_name).write_text(CSS)
    path = lambda l: LANGS[l][1] + "special-draw/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}special-draw/">'
    names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
    for lang, x in T.items():
        hl, pre = LANGS[lang]

        def fd(d, wd=True):
            if lang == "zh":
                return f"{d.year}年{d.month}月{d.day}日" + (f"（{WD['zh'][d.weekday()]}）" if wd else "")
            return (f"{WD[lang][d.weekday()]}, " if wd else "") + f"{d.day} {MON[lang][d.month - 1]} {d.year}"
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        logos = "".join(f'<i style="background-position:{-i * 22}px 0"></i>' for i in (0, 1, 2, 4, 5))
        if nxt:
            dd = (nxt - today).days
            cd = x["today"] if dd == 0 else x["tom"] if dd == 1 else x["days"].format(n=dd)
            mo = (f"{nxt.month}月" if lang == "zh" else MON["en" if lang == "ta" else lang][nxt.month - 1].upper())
            nxh = (f'<div class="nx"><div class="cal"><small>{mo}</small><b>{nxt.day}</b><span>{WD[lang][nxt.weekday()]}</span></div>'
                   f'<div><small>{esc(x["nx"])}</small><strong>{esc(fd(nxt))}</strong><span style="color:#C9D4EA">7:00pm</span> <em data-sd="{nxt.isoformat()}">{esc(cd)}</em><div class="lg">{logos}</div></div></div>')
            nxs = x["nxs"].format(d=fd(nxt))
        else:
            nxh, nxs = f'<p class="nx">{esc(x["none"])}</p>', x["none"]
        rows = ""
        for d in [d for d in allsp if d.year == yr]:
            k = d.strftime("%Y%m%d")
            st = (f'<a class="ok" href="{site.u("keputusan/" + d.isoformat() + "/")}">✓ {esc(x["done"])}</a>' if k in m else f'<span class="up">{esc(x["up"])}</span>')
            rows += f"<tr><td>{esc(fd(d, False))}</td><td>{WD[lang][d.weekday()]}</td><td>{st}</td></tr>"
        sch = f'<h2>{esc(x["sch"].format(y=yr))}</h2><div class="card"><table><tr>' + "".join(f"<th>{esc(c)}</th>" for c in x["st"]) + f"</tr>{rows}</table></div>"
        arch = f'<h2>{esc(x["arch"])}</h2><p class="lead" style="margin:0">{esc(x["archs"])}</p>'
        for y in sorted({d.year for d in past if d.year < yr}, reverse=True):
            arch += f'<div class="yr"><h3>{y}</h3><div class="ds">' + "".join(
                f'<a href="{site.u("keputusan/" + d.isoformat() + "/")}"><b>{esc(fd(d, False))}</b><small>{esc(x["m1"])} <span>{m[d.strftime("%Y%m%d")][2][0]}</span></small></a>'
                for d in sorted([d for d in past if d.year == y], reverse=True)) + "</div></div>"
        faq = [(q, a.replace("{next}", nxs)) for q, a in x["faq"]]
        faqh = f'<h2>{esc(x["fh"])}</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
        what = f'<h2>{esc(x["what"])}</h2>' + "".join(f"<p>{esc(p)}</p>" for p in x["p"])
        js = ('<script>(function(){var e=document.querySelector("[data-sd]");if(!e)return;var t=new Date(Date.now()+288e5),a=Date.UTC(t.getUTCFullYear(),t.getUTCMonth(),t.getUTCDate()),'
              'p=e.dataset.sd.split("-"),b=Date.UTC(+p[0],p[1]-1,+p[2]),n=Math.round((b-a)/864e5);if(n>1)e.textContent=' + json.dumps(x["days"]) + '.replace("{n}",n);'
              'else if(n===1)e.textContent=' + json.dumps(x["tom"]) + ';else if(n===0)e.textContent=' + json.dumps(x["today"]) + '})()</script>')
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        body = (f'<div class="sdp">{lng}{bc}<h1>{esc(x["h1"])}</h1><p class="lead">{esc(x["lead"])}</p>{nxh}{sch}{what}{arch}{faqh}'
                f'<div class="rp">{esc(x["rp"])}</div></div>{js}')
        fld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": hl,
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"], body, lang=hl, ld=[bld, fld],
                  head=f'<link rel="stylesheet" href="{site.u(css_name)}">' + alts)
