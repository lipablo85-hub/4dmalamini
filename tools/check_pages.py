"""/check-4d-number/ — the crawlable landing page for "semak nombor 4D" / "check 4D number".

The check tool itself lives behind ?tab=check on the app, which search engines cannot rank.
This page ranks for the intent, explains exactly what the check returns, and hands the visitor
straight into the number page for the digits they type.
"""
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
SLUG = "check-4d-number"

T = {
 "en": dict(
   home="Home", crumb="Check a 4D number",
   title="Check 4D Number — Past Wins, Last Seen & Frequency | 4D Malam Ini",
   desc="Check any 4D number against {n} draws since {y}. See every win, which company, which prize, days since the last win and all Box permutations.",
   h1="Check a 4D number", sub="Semak nombor 4D · 查万字成绩 · 4D எண் சரிபார்ப்பு",
   lead="Type four digits. You get every time that number has won in Malaysia since {y} — {n} draws across ten companies — not just tonight's result.",
   ph="0000", go="Check this number",
   err="Enter exactly four digits, 0000 to 9999.",
   wh="What the check gives you",
   items=[("Every win since {y}", "Each date the number was drawn, which company drew it and which prize it took — first, second, third, special or consolation."),
          ("Days since the last win", "How long the number has been quiet, counted to today."),
          ("How often it wins", "Total wins, broken down by year and by company, as a chart."),
          ("All Box permutations", "Every other order of the same four digits, with the win count for each, so a Box bet is easy to judge."),
          ("What the number means", "The 万字图 dictionary entry in Malay, English, Chinese and Tamil.")],
   eg="Try one of these", egs="Or browse the dictionary by range",
   fh="Common questions",
   faq=[("How do I check if my 4D number won?",
         "Type the four digits above. The number's page lists every draw it has won since {y}, with the date, the company and the prize. For tonight's result, the live board on the home page updates from 7pm."),
        ("Does a number that has not appeared for a long time become due?",
         "No. Every draw is independent, so a long gap changes nothing about the next draw. The days-since figure is a record of what happened, not a forecast."),
        ("What is a Box bet?",
         "A Box bet covers every order of the same four digits. 1234 Box also wins on 4321, 2143 and the rest. Each number page lists the permutations and how often each has won."),
        ("How far back does the history go?",
         "To {y}. That is {n} draw dates across Magnum 4D, Da Ma Cai, Sports Toto, GD Lotto, 9 Lotto, Singapore 4D, Cash Sweep, Sandakan 4D and Super J3/J9."),
        ("Is the data official?",
         "No. It is an unofficial record compiled from the companies' own result pages. Confirm with the company before claiming a prize.")],
   more="Popular numbers", stats="4D statistics", arch="Results archive", dict_="4D dictionary"),
 "ms": dict(
   home="Utama", crumb="Semak nombor 4D",
   title="Semak Nombor 4D — Sejarah Menang & Kekerapan | 4D Malam Ini",
   desc="Semak mana-mana nombor 4D dengan {n} cabutan sejak {y}. Lihat setiap kemenangan, syarikat, hadiah, hari sejak menang terakhir dan semua susunan Box.",
   h1="Semak nombor 4D", sub="Check a 4D number · 查万字成绩 · 4D எண் சரிபார்ப்பு",
   lead="Taip empat digit. Anda dapat setiap kali nombor itu menang di Malaysia sejak {y} — {n} cabutan daripada sepuluh syarikat — bukan keputusan malam ini sahaja.",
   ph="0000", go="Semak nombor ini",
   err="Masukkan tepat empat digit, 0000 hingga 9999.",
   wh="Apa yang anda dapat",
   items=[("Setiap kemenangan sejak {y}", "Setiap tarikh nombor itu dicabut, syarikat mana dan hadiah mana — pertama, kedua, ketiga, istimewa atau saguhati."),
          ("Hari sejak menang terakhir", "Berapa lama nombor itu sunyi, dikira hingga hari ini."),
          ("Kekerapan menang", "Jumlah kemenangan, dipecahkan mengikut tahun dan syarikat, dalam bentuk carta."),
          ("Semua susunan Box", "Setiap susunan lain bagi empat digit yang sama, dengan kiraan menang setiap satu, supaya taruhan Box mudah dinilai."),
          ("Maksud nombor", "Entri kamus 万字图 dalam Bahasa Melayu, English, 中文 dan தமிழ்.")],
   eg="Cuba salah satu", egs="Atau cari kamus mengikut julat",
   fh="Soalan lazim",
   faq=[("Bagaimana saya semak jika nombor 4D saya menang?",
         "Taip empat digit di atas. Halaman nombor itu menyenaraikan setiap cabutan yang dimenanginya sejak {y}, lengkap dengan tarikh, syarikat dan hadiah. Untuk keputusan malam ini, papan langsung di halaman utama dikemas kini dari jam 7 malam."),
        ("Adakah nombor yang lama tidak keluar akan tiba masanya?",
         "Tidak. Setiap cabutan adalah bebas, jadi jarak yang lama tidak mengubah apa-apa tentang cabutan seterusnya. Angka hari sejak menang terakhir ialah rekod apa yang berlaku, bukan ramalan."),
        ("Apa itu taruhan Box?",
         "Taruhan Box meliputi setiap susunan empat digit yang sama. 1234 Box juga menang pada 4321, 2143 dan yang lain. Setiap halaman nombor menyenaraikan susunan dan kekerapan menang setiap satu."),
        ("Sejauh mana sejarah ini?",
         "Sejak {y}. Itu {n} tarikh cabutan merentasi Magnum 4D, Da Ma Cai, Sports Toto, GD Lotto, 9 Lotto, Singapore 4D, Cash Sweep, Sandakan 4D dan Super J3/J9."),
        ("Adakah data ini rasmi?",
         "Tidak. Ia rekod tidak rasmi yang dikumpul daripada laman keputusan syarikat sendiri. Sahkan dengan syarikat sebelum menuntut hadiah.")],
   more="Nombor popular", stats="Statistik 4D", arch="Arkib keputusan", dict_="Kamus 4D"),
 "zh": dict(
   home="首页", crumb="查万字号码",
   title="查万字号码 — 中奖记录、上次开出与频率 | 4D Malam Ini",
   desc="用 {y} 年以来 {n} 期开奖记录查任何万字号码：每次中奖、哪家公司、哪个奖项、距离上次中奖天数，以及全部 Box 排列。",
   h1="查万字号码", sub="Semak nombor 4D · Check a 4D number · 4D எண் சரிபார்ப்பு",
   lead="输入四个数字。您会看到该号码自 {y} 年以来在马来西亚的每一次中奖 — 十家公司共 {n} 期 — 而不只是今晚的成绩。",
   ph="0000", go="查这个号码",
   err="请输入四位数字，0000 至 9999。",
   wh="您会看到什么",
   items=[("{y} 年以来每次中奖", "该号码每一次开出的日期、由哪家公司开出、中的是哪个奖项 — 头奖、二奖、三奖、特别奖或安慰奖。"),
          ("距离上次中奖天数", "该号码沉寂了多久，计算到今天。"),
          ("中奖频率", "总中奖次数，按年份和公司分列，以图表显示。"),
          ("全部 Box 排列", "相同四个数字的其他所有排列，以及各自的中奖次数，方便判断 Box 投注。"),
          ("号码含义", "万字图词条，提供马来文、英文、中文和淡米尔文四种语言。")],
   eg="试试这些", egs="或按号码范围浏览万字图",
   fh="常见问题",
   faq=[("怎样查我的万字号码有没有中奖？",
         "在上面输入四个数字。该号码的页面会列出它自 {y} 年以来中过的每一期，包含日期、公司和奖项。今晚的成绩请看首页的即时成绩板，晚上 7 点起更新。"),
        ("很久没开的号码是不是快要开了？",
         "不是。每一期开奖都是独立的，间隔再长也不会改变下一期的结果。距离上次中奖的天数是已发生事实的记录，不是预测。"),
        ("什么是 Box 投注？",
         "Box 投注涵盖相同四个数字的所有排列。1234 Box 在开出 4321、2143 等时同样中奖。每个号码页面都列出排列及各自的中奖次数。"),
        ("记录可以追溯到多久以前？",
         "{y} 年。共 {n} 个开奖日期，涵盖万能、大马彩、多多、豪龙、9 Lotto、新加坡万字、砂拉越大万、山打根和 Super J3/J9。"),
        ("这些数据是官方的吗？",
         "不是。这是根据各公司成绩页面整理的非官方记录。兑奖前请向公司核实。")],
   more="热门号码", stats="万字统计", arch="成绩记录", dict_="万字图"),
 "ta": dict(
   home="முகப்பு", crumb="4D எண் சரிபார்ப்பு",
   title="4D எண் சரிபார்ப்பு — வெற்றி வரலாறு & அதிர்வெண் | 4D Malam Ini",
   desc="{y} முதல் {n} குலுக்கல்களுடன் எந்த 4D எண்ணையும் சரிபாருங்கள்: ஒவ்வொரு வெற்றி, நிறுவனம், பரிசு, கடைசி வெற்றிக்குப் பிந்தைய நாட்கள், Box வரிசைகள்.",
   h1="4D எண் சரிபார்ப்பு", sub="Semak nombor 4D · Check a 4D number · 查万字成绩",
   lead="நான்கு இலக்கங்களைத் தட்டச்சு செய்யுங்கள். {y} முதல் மலேசியாவில் அந்த எண் வென்ற ஒவ்வொரு முறையும் தெரியும் — பத்து நிறுவனங்களில் {n} குலுக்கல்கள்.",
   ph="0000", go="இந்த எண்ணைச் சரிபார்",
   err="சரியாக நான்கு இலக்கங்கள் உள்ளிடவும், 0000 முதல் 9999 வரை.",
   wh="நீங்கள் பெறுவது",
   items=[("{y} முதல் ஒவ்வொரு வெற்றியும்", "எண் வந்த ஒவ்வொரு தேதி, எந்த நிறுவனம், எந்தப் பரிசு — முதல், இரண்டாம், மூன்றாம், சிறப்பு அல்லது ஆறுதல்."),
          ("கடைசி வெற்றிக்குப் பிந்தைய நாட்கள்", "அந்த எண் எவ்வளவு காலம் அமைதியாக உள்ளது, இன்று வரை."),
          ("எவ்வளவு அடிக்கடி வெல்கிறது", "மொத்த வெற்றிகள், ஆண்டு வாரியாகவும் நிறுவனம் வாரியாகவும் வரைபடமாக."),
          ("அனைத்து Box வரிசைகள்", "அதே நான்கு இலக்கங்களின் மற்ற எல்லா வரிசைகளும், ஒவ்வொன்றின் வெற்றி எண்ணிக்கையுடன்."),
          ("எண்ணின் பொருள்", "万字图 அகராதி உள்ளீடு — மலாய், ஆங்கிலம், சீனம், தமிழ்.")],
   eg="இவற்றில் ஒன்றை முயலுங்கள்", egs="அல்லது வரம்பு வாரியாக அகராதியைப் பாருங்கள்",
   fh="பொதுவான கேள்விகள்",
   faq=[("என் 4D எண் வென்றதா என எப்படிச் சரிபார்ப்பது?",
         "மேலே நான்கு இலக்கங்களைத் தட்டச்சு செய்யுங்கள். {y} முதல் அது வென்ற ஒவ்வொரு குலுக்கலும் தேதி, நிறுவனம், பரிசுடன் பட்டியலிடப்படும். இன்றிரவு முடிவுக்கு முகப்புப் பக்கம் இரவு 7 மணி முதல் புதுப்பிக்கப்படும்."),
        ("நீண்ட நாட்களாக வராத எண் விரைவில் வருமா?",
         "இல்லை. ஒவ்வொரு குலுக்கலும் தனித்தனி, எனவே நீண்ட இடைவெளி அடுத்த குலுக்கலை மாற்றாது. நாட்கள் எண்ணிக்கை நடந்ததன் பதிவு, முன்னறிவிப்பு அல்ல."),
        ("Box பந்தயம் என்றால் என்ன?",
         "Box பந்தயம் அதே நான்கு இலக்கங்களின் எல்லா வரிசைகளையும் உள்ளடக்கும். 1234 Box என்பது 4321, 2143 வந்தாலும் வெல்லும். ஒவ்வொரு எண் பக்கமும் வரிசைகளைப் பட்டியலிடுகிறது."),
        ("வரலாறு எவ்வளவு பின்னோக்கி செல்கிறது?",
         "{y} வரை. Magnum 4D, Da Ma Cai, Sports Toto, GD Lotto, 9 Lotto, Singapore 4D, Cash Sweep, Sandakan 4D, Super J3/J9 ஆகியவற்றில் {n} குலுக்கல் தேதிகள்."),
        ("இந்தத் தரவு அதிகாரப்பூர்வமானதா?",
         "இல்லை. நிறுவனங்களின் சொந்த முடிவுப் பக்கங்களிலிருந்து தொகுக்கப்பட்ட அதிகாரப்பூர்வமற்ற பதிவு. பரிசு கோருவதற்கு முன் நிறுவனத்துடன் உறுதிப்படுத்தவும்.")],
   more="பிரபல எண்கள்", stats="4D புள்ளிவிவரம்", arch="முடிவுகள் காப்பகம்", dict_="4D அகராதி"),
}

CSS = """.chk{max-width:640px}
.chk .lead{font-size:15.5px;line-height:1.6;color:#C9D4EA;margin:10px 0 18px}
.chk form{display:flex;gap:8px;margin:0 0 6px}
.chk input{flex:1;min-width:0;height:60px;border-radius:16px;border:1.5px solid #2C4A7E;background:#0F1F3D;color:#F8F4E8;
 font:700 30px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.28em;text-align:center;padding:0 0 0 .28em;outline:none}
.chk input:focus{border-color:#E9C46B;box-shadow:0 0 0 3px rgba(233,196,107,.18)}
.chk button{flex:none;height:60px;padding:0 20px;border:0;border-radius:16px;background:#E9C46B;color:#07142B;font:700 15px/1 inherit;cursor:pointer}
.chk .er{font-size:12.5px;color:#FF8A8F;min-height:18px;margin:0 0 14px}
.chk ul.wh{list-style:none;padding:0;margin:12px 0 0;display:grid;gap:9px}
.chk ul.wh li{background:#0F1F3D;border:1px solid #233862;border-radius:14px;padding:11px 13px}
.chk ul.wh b{display:block;font-size:14px;margin-bottom:2px}
.chk ul.wh span{font-size:13px;color:#9FB0D3;line-height:1.5}
.chk .eg{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0}
.chk .eg a{display:inline-flex;flex-direction:column;align-items:center;min-width:76px;padding:9px 12px;border-radius:12px;
 background:#0F1F3D;border:1px solid #233862;text-decoration:none;color:#F8F4E8;font:700 17px/1.1 ui-monospace,Menlo,monospace;letter-spacing:.06em}
.chk .eg a small{font:600 11px/1.3 system-ui,sans-serif;color:#9FB0D3;letter-spacing:0;margin-top:3px}
.chk details{background:#0F1F3D;border:1px solid #233862;border-radius:14px;margin:8px 0;overflow:hidden}
.chk summary{padding:12px 14px;cursor:pointer;font-weight:700;font-size:14px;list-style:none}
.chk summary::-webkit-details-marker{display:none}
.chk summary::after{content:"+";float:right;color:#E9C46B;font-weight:700}
.chk details[open] summary::after{content:"–"}
.chk details p{margin:0;padding:0 14px 13px;font-size:13.5px;color:#9FB0D3;line-height:1.55}
.chk .cta{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0}
.chk .cta a{flex:1 1 44%;min-height:48px;display:flex;align-items:center;justify-content:center;border-radius:13px;
 background:#172A4D;color:#F8F4E8;text-decoration:none;font-size:13.5px;font-weight:700;text-align:center;padding:0 10px}
@media(min-width:620px){.chk ul.wh{grid-template-columns:1fr 1fr}}"""

JS = ("<script>(function(){var f=document.getElementById('cf'),i=document.getElementById('cn'),e=document.getElementById('ce'),m=%s;"
      "i.addEventListener('input',function(){i.value=i.value.replace(/\\D/g,'').slice(0,4);e.textContent=''});"
      "f.addEventListener('submit',function(ev){ev.preventDefault();var v=i.value;"
      "if(!/^\\d{4}$/.test(v)){e.textContent=m;i.focus();return}location.href='/4d/'+v+'/'})})()</script>")

EGS = [("8888", "发发发发"), ("1314", "一生一世"), ("5201", "我爱你"), ("6888", "顺发发发")]


def build(site) -> None:
    import hashlib, json
    from seo_pages import d8
    css = "assets/ck." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / css).write_text(CSS)
    n, y = f"{len(site.dates):,}", d8(site.dates[0]).year
    lastmod = d8(site.dates[-1]).isoformat()
    for lang, (hl, pre) in LANGS.items():
        x = T[lang]
        f = lambda s: s.format(n=n, y=y)
        items = "".join(f'<li><b>{esc(f(a))}</b><span>{esc(f(b))}</span></li>' for a, b in x["items"])
        egs = "".join(f'<a href="{site.u(f"4d/{num}/")}">{num}<small>{esc(mean)}</small></a>' for num, mean in EGS)
        faq = [(f(q), f(a)) for q, a in x["faq"]]
        det = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
        nav, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        cta = "".join(f'<a href="{site.u(h)}">{esc(t)}</a>' for t, h in (
            (x["more"], pre + "popular-4d-numbers/"), (x["stats"], pre + "4d-statistics/"),
            (x["arch"], "keputusan/"), (x["dict_"], "4d/")))
        body = (f'<div class="chk">{nav}<h1>{esc(x["h1"])}<small>{esc(x["sub"])}</small></h1>'
                f'<p class="lead">{esc(f(x["lead"]))}</p>'
                f'<form id="cf"><input id="cn" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" '
                f'placeholder="{x["ph"]}" aria-label="{esc(x["h1"])}" autocomplete="off"><button type="submit">{esc(x["go"])}</button></form>'
                f'<p class="er" id="ce" role="alert"></p>'
                f'<h2>{esc(x["wh"])}</h2><ul class="wh">{items}</ul>'
                f'<h2>{esc(x["eg"])}</h2><div class="eg">{egs}</div>'
                f'<p style="margin-top:14px"><a href="{site.u("4d/")}" style="color:#E9C46B">{esc(x["egs"])} ›</a></p>'
                f'<h2>{esc(x["fh"])}</h2>{det}'
                f'<div class="cta">{cta}</div></div>')
        fql = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": hl,
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": x["h1"], "inLanguage": hl,
               "url": site.site + f"{pre}{SLUG}/", "applicationCategory": "UtilitiesApplication",
               "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "MYR"},
               "description": f(x["desc"]),
               "publisher": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site}}
        alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{LANGS[l][1]}{SLUG}/">' for l in LANGS) \
            + f'<link rel="alternate" hreflang="x-default" href="{site.site}{SLUG}/">'
        site.page(f"{pre}{SLUG}/", f(x["title"]), f(x["desc"]), body, hl, [bld, fql, app], lastmod,
                  head=f'<link rel="stylesheet" href="{site.u(css)}">' + alts,
                  foot=JS % json.dumps(x["err"]))
