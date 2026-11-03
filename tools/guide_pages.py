"""4D how-to-play guide: a hub page and one page per operator, in 4 languages.
URLs: /guide/ (EN), /ms/guide/, /zh/guide/, /ta/guide/  +  .../magnum-4d/, .../sports-toto-4d/, .../da-ma-cai-1-3d/
Written in our own words from the operators' official how-to-play pages (linked on every page).
Prize figures: Da Ma Cai's official 1+3D prize table (per RM1); Magnum and Sports Toto use the same Big/Small structure.
"""
from seo_pages import esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
OPS = [  # slug, key, name, colour, official how-to-play URL
    ("magnum-4d", "M", "Magnum 4D", "#E9C46B", "https://support.magnum4d.my/hc/en-us/sections/360001123776-How-To-Play"),
    ("sports-toto-4d", "T", "Sports Toto 4D", "#FF5A5F", "https://www.sportstoto.com.my/how_to_play_4dJ.asp"),
    ("da-ma-cai-1-3d", "D", "Da Ma Cai 1+3D", "#4C8DFF", "https://www.damacai.com.my/how-to-play/"),
]

CSS = """@font-face{font-family:"Jakarta";src:url(__FONT__) format("woff2");font-weight:200 800;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
body{font-family:"Jakarta",system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans","Noto Sans Tamil","PingFang SC","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.gd{font-size:16px;line-height:1.7;color:#D5DCEA;padding-bottom:24px}
.gd p{margin:0 0 12px}.gd strong{color:#F8F4E8;font-weight:700}
.gd a{color:#E9C46B;text-underline-offset:3px;text-decoration-thickness:1px}
.top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:14px 0 4px}.top .bc{margin:0}
.lng{display:inline-flex;gap:2px;background:#0F1F3D;border:1px solid #233862;border-radius:999px;padding:3px}
.lng a{min-width:40px;height:32px;display:inline-grid;place-items:center;padding:0 10px;border-radius:999px;color:#A9B4CC;text-decoration:none;font-size:12px;font-weight:800}
.lng a[aria-current]{background:#F8F4E8;color:#07142B}
.hero{margin:18px 0 6px;padding:22px 18px;border-radius:22px;background:radial-gradient(120% 140% at 0% 0%,#1C3567 0%,#0F1F3D 55%,#0B1934 100%);border:1px solid #233862}
.hero .kick{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#E9C46B;margin-bottom:8px}
.gd h1{font-size:clamp(26px,7vw,34px);line-height:1.15;letter-spacing:-.02em;font-weight:800;margin:0;color:#F8F4E8}
.gd h1 small{display:block;margin-top:10px;font-size:15px;line-height:1.55;font-weight:500;color:#A9B4CC;letter-spacing:0}
.toc{position:sticky;top:0;z-index:3;display:flex;gap:8px;overflow-x:auto;margin:0 -16px;padding:10px 16px;background:rgba(7,20,43,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);scrollbar-width:none;border-bottom:1px solid #1A2C50}
.toc::-webkit-scrollbar{display:none}
.toc a{flex:none;min-height:38px;display:inline-flex;align-items:center;gap:6px;padding:0 14px;border-radius:999px;background:#0F1F3D;border:1px solid #233862;color:#F8F4E8;text-decoration:none;font-size:13px;font-weight:700}
.toc a b{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#E9C46B;color:#07142B;font-size:11px}
.st{scroll-margin-top:70px;margin-top:16px;padding:20px 18px 8px;border-radius:20px;background:#0F1F3D;border:1px solid #1E3361}
.st h2{display:grid;grid-template-columns:34px 1fr;align-items:center;gap:12px;margin:0 0 12px;font-size:19px;line-height:1.3;font-weight:800;letter-spacing:-.01em;color:#F8F4E8}
.st h2 i{display:grid;place-items:center;width:34px;height:34px;border-radius:11px;background:#E9C46B;color:#07142B;font-style:normal;font-size:16px;font-weight:800}
.gd ul{list-style:none;padding:0;margin:0 0 14px}
.gd li{position:relative;padding:0 0 0 22px;margin:0 0 10px}
.gd li::before{content:"";position:absolute;left:4px;top:.68em;width:7px;height:7px;border-radius:50%;background:#E9C46B}
.tbl{margin:4px 0 14px;border-radius:16px;overflow:hidden;border:1px solid #233862;background:#0B1934}
.tbl table{width:100%;border-collapse:collapse;font-size:15px}
.tbl caption{caption-side:top;text-align:left;padding:12px 14px 4px;font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#A9B4CC}
.tbl th,.tbl td{padding:12px 14px;border-bottom:1px solid #1A2C50;text-align:left;vertical-align:middle}
.tbl tr:last-child th,.tbl tr:last-child td{border-bottom:0}
.tbl thead th{font-size:12px;font-weight:800;color:#A9B4CC;background:#0F1F3D;text-transform:uppercase;letter-spacing:.04em}
.tbl tbody th{font-weight:600;color:#F8F4E8;font-size:14px}
.tbl .n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:800;color:#F8F4E8}
.tbl .n.big{color:#E9C46B}.tbl .n.na{color:#5A6A8C;font-weight:600}
.tbl .mono{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;letter-spacing:.06em;color:#E9C46B}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 14px}
.duo div{padding:14px;border-radius:14px;background:#0B1934;border:1px solid #233862;font-size:14px;line-height:1.5}
.duo b{display:block;font-size:17px;color:#F8F4E8;margin-bottom:4px}.duo .cnt{display:inline-block;margin-top:8px;padding:2px 8px;border-radius:999px;background:#172A4D;color:#E9C46B;font-size:12px;font-weight:800}
.note{position:relative;background:#13254A;border:1px solid #2A4475;border-radius:14px;padding:14px 14px 14px 48px;margin:4px 0 14px;font-size:15px;line-height:1.6}
.note::before{content:"i";position:absolute;left:14px;top:15px;display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#E9C46B;color:#07142B;font-weight:800;font-size:13px;font-style:italic}
.note.warn::before{content:"!";font-style:normal;background:#FF8A65}
.opg{display:grid;gap:10px;margin:0 0 14px}
.opg a{display:grid;grid-template-columns:40px 1fr 18px;align-items:center;gap:12px;min-height:64px;padding:10px 14px;border-radius:16px;background:#0B1934;border:1px solid #233862;border-left:5px solid var(--c);color:#F8F4E8;text-decoration:none}
.opg img{width:40px;height:40px;object-fit:contain}.opg b{display:block;font-size:16px;line-height:1.3;color:#F8F4E8}.opg span span{display:block;font-size:13px;color:#A9B4CC;font-weight:500}
.opg a::after{content:"›";font-size:24px;color:#A9B4CC;line-height:1}
.ext{display:grid;gap:8px;margin:0 0 14px}.ext a{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:50px;padding:0 14px;border-radius:14px;background:#0B1934;border:1px solid #233862;color:#F8F4E8;text-decoration:none;font-weight:600;font-size:15px}
.ext a::after{content:"↗";color:#E9C46B}
.cta{display:grid;gap:10px;margin:18px 0}
.cta a{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:14px;font-weight:800;text-decoration:none;font-size:16px;text-align:center;padding:0 16px}
.cta .p{background:#E9C46B;color:#07142B}.cta .s{background:#172A4D;color:#F8F4E8;border:1px solid #233862}
.ophero{display:flex;align-items:center;gap:14px;margin:18px 0 6px;padding:18px;border-radius:22px;background:#0F1F3D;border:1px solid #233862;box-shadow:inset 0 5px 0 var(--c)}
.ophero img{width:56px;height:56px;object-fit:contain;flex:none}
.ophero h1{font-size:clamp(22px,6vw,30px)}.ophero h1 small{margin-top:6px;font-size:14px}
.back{display:inline-flex;align-items:center;min-height:44px;font-weight:700}
@media(min-width:720px){.st{padding:26px 26px 12px}.hero{padding:30px 28px}.cta{grid-template-columns:1fr 1fr}.toc{margin:0;border-radius:0 0 14px 14px}}
@media(max-width:380px){.duo{grid-template-columns:1fr}.tbl th,.tbl td{padding:11px 10px}}"""

# ---------------- text per language ----------------
T = {
"en": dict(
  home="Home", guide="4D Guide", title="How to Play 4D in Malaysia: Big, Small & Box",
  desc="Simple guide to playing 4D in Malaysia: Big vs Small, prize per RM1, Box, iBox and Roll bets, chances of winning, draw days and how to check results.",
  h1="How to play 4D in Malaysia", sub="Big and Small, prizes per RM1, Box and iBox, and your real chances — explained simply.",
  toc=[("pick", "Pick a number"), ("bigsmall", "Big or Small"), ("ways", "Box & iBox"), ("odds", "Chances"), ("days", "Draw days"), ("rules", "Rules")],
  s1="Pick a 4-digit number", p1="Any number from <strong>0000</strong> to <strong>9999</strong> — 10,000 possible numbers. Many players use birthdays, car plates or a dream looked up in the <a href=\"{dict}\">4D dictionary 万字图</a>. Every number has exactly the same chance in each draw.",
  s2="Choose Big or Small", p2="Each draw gives 23 winning numbers: 1st, 2nd and 3rd prize, 10 Special (also called Starter) and 10 Consolation.",
  big="<strong>Big</strong> wins on all 23 numbers. Smaller top prizes, more ways to win.", small="<strong>Small</strong> wins only on 1st, 2nd and 3rd. Bigger top prizes, fewer ways to win.",
  tcap="Prize for every RM1 bet", tprize="Prize", tbig="Big", tsmall="Small", rows=["1st Prize", "2nd Prize", "3rd Prize", "Special / Starter (10)", "Consolation (10)"],
  ex="<strong>Example:</strong> RM2 Big on 1234. If 1234 comes out as 2nd prize you get 2 × RM1,000 = <strong>RM2,000</strong>. If it is one of the Special numbers you get 2 × RM180 = <strong>RM360</strong>. A Small bet on the same number would win nothing for Special.",
  s3="Other ways to play: Box, iBox and Roll", p3="A <strong>Straight</strong> bet wins only when the digits come out in your exact order. To cover other orders of the same digits:",
  ways=["<strong>Box</strong> — buys every order of your digits as separate bets, so it costs more (RM24 for 1234 at RM1 each) but each win pays the full prize.", "<strong>iBox</strong> — covers every order for one stake (from RM1). Any order can win, but the prize is divided by the number of orders.", "<strong>Roll</strong> — one position becomes 0–9, e.g. 12R4 covers 1204, 1214 … 1294: 10 numbers for RM10."],
  pcap="How many orders a number has", pt=["Digits", "Example", "Orders"], prow=[("All different", "1234", "24"), ("One pair", "1123", "12"), ("Two pairs", "1122", "6"), ("Three the same", "1112", "4")],
  pnote="Names and minimum bets differ a little between companies — Da Ma Cai calls these B24/IB24, for example. Check the company's own page before you play.",
  s4="Your real chances", p4="With 10,000 numbers and 23 prizes, one RM1 Big ticket has about <strong>1 in 435</strong> chance of winning anything, and about <strong>1 in 3,333</strong> for Small. Over many draws the prizes pay back roughly <strong>64–65 sen for every RM1</strong> spent. Treat 4D as entertainment with a cost, never as income.",
  s5="Draw days and results", p5="Magnum, Sports Toto and Da Ma Cai draw every <strong>Wednesday, Saturday and Sunday at 7pm</strong>, plus special draws they announce (often on a Tuesday). GD Lotto and 9 Lotto draw every evening. Results appear on <a href=\"{home}\">4D Malam Ini</a> from 7pm with all companies on one board, and you can <a href=\"{check}\">check any number</a> against five years of draws.",
  s6="Who can play and claiming prizes", rules=["Only <strong>non-Muslims aged 21 and above</strong> may buy tickets or claim prizes.", "Buy only from licensed outlets of the companies. Tickets from third parties or illegal bookies are not paid and buying them is an offence.", "Keep your ticket safe and check the claim rules and deadline on the company's official page.", "Set a budget, never chase losses, and take a break if it stops being fun."],
  s7="Guide by company", s8="Official how-to-play pages", official="The rules and prize amounts on the company's official page always take priority over this guide.",
  opdesc={"M": "Draws Wed, Sat, Sun · 7pm", "T": "Draws Wed, Sat, Sun · 7pm", "D": "Draws Wed, Sat, Sun · 7pm"},
  op=dict(
    M=("How to play Magnum 4D", "Magnum 4D: Big, Small, prizes per RM1 and draw days explained simply, with a link to Magnum's official how-to-play page.",
       "Magnum 4D is the classic 4D game from Magnum, the first private company licensed to run 4D in Malaysia. You pick a number from 0000 to 9999, choose Big or Small and the amount.",
       ["Big covers all 23 winning numbers; Small covers only 1st, 2nd and 3rd.", "Prize per RM1: Big RM2,500 / 1,000 / 500, Special RM180, Consolation RM60. Small RM3,500 / 2,000 / 1,000.", "Magnum also runs 4D Jackpot and other games with their own rules — see Magnum's official page.", "Tickets can be bought for upcoming draws in advance at Magnum outlets."]),
    T=("How to play Sports Toto 4D", "Sports Toto 4D: how Big and Small work, prize per RM1, Box and iBox and draw days, with a link to Sports Toto's official guide.",
       "Sports Toto 4D works like the other Malaysian 4D games: pick 0000–9999, choose Big or Small and your stake. Sports Toto also runs 4D Jackpot, 5D, 6D and Toto lotto games with separate rules.",
       ["Big covers 23 winning numbers; Small covers the top 3.", "Prize per RM1: Big RM2,500 / 1,000 / 500, Special RM180, Consolation RM60. Small RM3,500 / 2,000 / 1,000.", "Box and iBox let you cover every order of your digits — see the table in the main guide.", "4D Jackpot rules and prizes are on Sports Toto's official page."]),
    D=("How to play Da Ma Cai 1+3D", "Da Ma Cai 1+3D explained: ABC (Big) and A (Small), Starter prizes, Box, iBox (IB24/IB12/IB6/IB4) and Roll bets, prize per RM1.",
       "Da Ma Cai's 4D game is called 1+3D. Its bet types use letters: <strong>ABC</strong> is Big (all 23 numbers) and <strong>A</strong> is Small (1st, 2nd, 3rd only). Special prizes are called <strong>Starter</strong>.",
       ["Minimum RM1 for a straight bet.", "Box: B24 / B12 / B6 / B4 cost RM24 / RM12 / RM6 / RM4 and pay the full prize.", "iBox: IB24 / IB12 / IB6 / IB4 from RM1; e.g. an IB24 Big 1st prize pays RM105 per RM1.", "Roll bet from RM10; Lucky Pick (random number) from RM1."]),
  ),
  checkbtn="Check a 4D number", back="← Back to 4D Guide", res="See the latest results", lnk="Official page",
),
"ms": dict(
  home="Utama", guide="Panduan 4D", title="Cara Main 4D: Big, Small, Box & Hadiah",
  desc="Panduan mudah cara main 4D di Malaysia: Big lawan Small, hadiah setiap RM1, Box, iBox dan Roll, peluang menang, hari cabutan dan cara semak keputusan.",
  h1="Cara main 4D di Malaysia", sub="Big dan Small, hadiah setiap RM1, Box dan iBox, serta peluang sebenar anda — diterangkan dengan mudah.",
  toc=[("pick", "Pilih nombor"), ("bigsmall", "Big atau Small"), ("ways", "Box & iBox"), ("odds", "Peluang"), ("days", "Hari cabutan"), ("rules", "Peraturan")],
  s1="Pilih nombor 4 digit", p1="Mana-mana nombor dari <strong>0000</strong> hingga <strong>9999</strong> — 10,000 nombor. Ramai pemain guna tarikh lahir, nombor plat kereta atau mimpi yang dicari dalam <a href=\"{dict}\">kamus 4D 万字图</a>. Setiap nombor ada peluang yang sama dalam setiap cabutan.",
  s2="Pilih Big atau Small", p2="Setiap cabutan ada 23 nombor menang: hadiah pertama, kedua dan ketiga, 10 Special (juga dipanggil Starter) dan 10 Saguhati.",
  big="<strong>Big</strong> menang pada semua 23 nombor. Hadiah utama lebih kecil, lebih banyak peluang menang.", small="<strong>Small</strong> menang hanya pada hadiah 1, 2 dan 3. Hadiah utama lebih besar, peluang lebih sedikit.",
  tcap="Hadiah bagi setiap RM1", tprize="Hadiah", tbig="Big", tsmall="Small", rows=["Hadiah Pertama", "Hadiah Kedua", "Hadiah Ketiga", "Special / Starter (10)", "Saguhati (10)"],
  ex="<strong>Contoh:</strong> RM2 Big pada 1234. Jika 1234 keluar hadiah kedua, anda dapat 2 × RM1,000 = <strong>RM2,000</strong>. Jika ia salah satu nombor Special, anda dapat 2 × RM180 = <strong>RM360</strong>. Pertaruhan Small pada nombor sama tidak menang apa-apa untuk Special.",
  s3="Cara lain: Box, iBox dan Roll", p3="Pertaruhan <strong>Straight</strong> hanya menang jika digit keluar mengikut susunan tepat anda. Untuk meliputi susunan lain:",
  ways=["<strong>Box</strong> — membeli setiap susunan digit sebagai pertaruhan berasingan, jadi kosnya lebih tinggi (RM24 untuk 1234 pada RM1 setiap satu) tetapi setiap kemenangan dibayar hadiah penuh.", "<strong>iBox</strong> — meliputi setiap susunan dengan satu taruhan (dari RM1). Mana-mana susunan boleh menang, tetapi hadiah dibahagi dengan bilangan susunan.", "<strong>Roll</strong> — satu kedudukan menjadi 0–9, cth. 12R4 meliputi 1204, 1214 … 1294: 10 nombor untuk RM10."],
  pcap="Bilangan susunan bagi satu nombor", pt=["Digit", "Contoh", "Susunan"], prow=[("Semua berbeza", "1234", "24"), ("Satu pasang", "1123", "12"), ("Dua pasang", "1122", "6"), ("Tiga sama", "1112", "4")],
  pnote="Nama dan taruhan minimum berbeza sedikit antara syarikat — contohnya Da Ma Cai menggunakan B24/IB24. Semak halaman rasmi syarikat sebelum bermain.",
  s4="Peluang sebenar anda", p4="Dengan 10,000 nombor dan 23 hadiah, satu tiket Big RM1 ada peluang kira-kira <strong>1 dalam 435</strong> untuk menang apa-apa hadiah, dan <strong>1 dalam 3,333</strong> untuk Small. Dalam jangka panjang, hadiah membayar balik lebih kurang <strong>64–65 sen bagi setiap RM1</strong>. Anggap 4D sebagai hiburan yang ada kos, bukan sumber pendapatan.",
  s5="Hari cabutan dan keputusan", p5="Magnum, Sports Toto dan Da Ma Cai membuat cabutan setiap <strong>Rabu, Sabtu dan Ahad jam 7 malam</strong>, serta cabutan khas yang diumumkan (biasanya hari Selasa). GD Lotto dan 9 Lotto membuat cabutan setiap malam. Keputusan keluar di <a href=\"{home}\">4D Malam Ini</a> dari jam 7 malam dengan semua syarikat dalam satu papan, dan anda boleh <a href=\"{check}\">semak mana-mana nombor</a> dengan rekod lima tahun.",
  s6="Siapa boleh bermain dan tuntutan hadiah", rules=["Hanya <strong>bukan Islam berumur 21 tahun ke atas</strong> boleh membeli tiket atau menuntut hadiah.", "Beli hanya di cawangan berlesen syarikat. Tiket daripada pihak ketiga atau bookie haram tidak dibayar dan membelinya adalah satu kesalahan.", "Simpan tiket dengan selamat dan semak syarat serta tempoh tuntutan di halaman rasmi syarikat.", "Tetapkan bajet, jangan kejar kerugian, dan berehat jika tidak lagi seronok."],
  s7="Panduan mengikut syarikat", s8="Halaman rasmi cara bermain", official="Peraturan dan jumlah hadiah di halaman rasmi syarikat sentiasa mengatasi panduan ini.",
  opdesc={"M": "Cabutan Rabu, Sabtu, Ahad · 7 mlm", "T": "Cabutan Rabu, Sabtu, Ahad · 7 mlm", "D": "Cabutan Rabu, Sabtu, Ahad · 7 mlm"},
  op=dict(
    M=("Cara main Magnum 4D", "Magnum 4D: Big, Small, hadiah setiap RM1 dan hari cabutan diterangkan dengan mudah, dengan pautan ke halaman rasmi Magnum.",
       "Magnum 4D ialah permainan 4D klasik daripada Magnum, syarikat swasta pertama yang dilesenkan mengendalikan 4D di Malaysia. Pilih nombor 0000 hingga 9999, pilih Big atau Small dan jumlah taruhan.",
       ["Big meliputi semua 23 nombor menang; Small hanya hadiah 1, 2 dan 3.", "Hadiah setiap RM1: Big RM2,500 / 1,000 / 500, Special RM180, Saguhati RM60. Small RM3,500 / 2,000 / 1,000.", "Magnum juga ada 4D Jackpot dan permainan lain dengan peraturan sendiri — lihat halaman rasmi Magnum.", "Tiket boleh dibeli lebih awal untuk cabutan akan datang di cawangan Magnum."]),
    T=("Cara main Sports Toto 4D", "Sports Toto 4D: cara Big dan Small berfungsi, hadiah setiap RM1, Box dan iBox serta hari cabutan, dengan pautan ke panduan rasmi Sports Toto.",
       "Sports Toto 4D sama seperti permainan 4D lain di Malaysia: pilih 0000–9999, pilih Big atau Small dan taruhan anda. Sports Toto juga ada 4D Jackpot, 5D, 6D dan Toto dengan peraturan berasingan.",
       ["Big meliputi 23 nombor menang; Small hanya 3 hadiah utama.", "Hadiah setiap RM1: Big RM2,500 / 1,000 / 500, Special RM180, Saguhati RM60. Small RM3,500 / 2,000 / 1,000.", "Box dan iBox meliputi setiap susunan digit anda — lihat jadual dalam panduan utama.", "Peraturan dan hadiah 4D Jackpot ada di halaman rasmi Sports Toto."]),
    D=("Cara main Da Ma Cai 1+3D", "Da Ma Cai 1+3D diterangkan: ABC (Big) dan A (Small), hadiah Starter, Box, iBox (IB24/IB12/IB6/IB4) dan Roll, hadiah setiap RM1.",
       "Permainan 4D Da Ma Cai dipanggil 1+3D. Jenis pertaruhannya guna huruf: <strong>ABC</strong> ialah Big (semua 23 nombor) dan <strong>A</strong> ialah Small (hadiah 1, 2, 3 sahaja). Hadiah Special dipanggil <strong>Starter</strong>.",
       ["Minimum RM1 untuk pertaruhan straight.", "Box: B24 / B12 / B6 / B4 berharga RM24 / RM12 / RM6 / RM4 dan dibayar hadiah penuh.", "iBox: IB24 / IB12 / IB6 / IB4 dari RM1; cth. IB24 Big hadiah pertama membayar RM105 setiap RM1.", "Roll dari RM10; Lucky Pick (nombor rawak) dari RM1."]),
  ),
  checkbtn="Semak nombor 4D", back="← Kembali ke Panduan 4D", res="Lihat keputusan terkini", lnk="Halaman rasmi",
),
"zh": dict(
  home="首页", guide="万字攻略", title="马来西亚万字怎么玩：大字、小字、Box 与奖金说明",
  desc="马来西亚万字（4D）入门：大字与小字的分别、每 RM1 奖金、Box、iBox 与 Roll 玩法、中奖机会、开彩日期与查询成绩。",
  h1="马来西亚万字（4D）怎么玩", sub="大字与小字、每 RM1 奖金、Box 与 iBox，以及真实的中奖机会，一次说清楚。",
  toc=[("pick", "选号码"), ("bigsmall", "大字或小字"), ("ways", "Box 与 iBox"), ("odds", "中奖机会"), ("days", "开彩日期"), ("rules", "规则")],
  s1="选一个4位数号码", p1="从 <strong>0000</strong> 到 <strong>9999</strong> 任选一个，共 10,000 个号码。很多人用生日、车牌，或在<a href=\"{dict}\">万字图</a>里查梦境对应的号码。每个号码在每期的机会都完全一样。",
  s2="选择大字或小字", p2="每期开出 23 个中奖号码：头奖、二奖、三奖，10 个特别奖（入围奖）和 10 个安慰奖。",
  big="<strong>大字（Big）</strong>：23 个号码都能中。头奖较小，但中奖途径多。", small="<strong>小字（Small）</strong>：只中头、二、三奖。头奖较大，但中奖途径少。",
  tcap="每下注 RM1 的奖金", tprize="奖项", tbig="大字", tsmall="小字", rows=["头奖", "二奖", "三奖", "特别奖 / 入围奖（10个）", "安慰奖（10个）"],
  ex="<strong>例子：</strong>1234 买大字 RM2。如果 1234 开出二奖，可得 2 × RM1,000 = <strong>RM2,000</strong>；如果是特别奖，可得 2 × RM180 = <strong>RM360</strong>。同一号码买小字，开特别奖则没有奖金。",
  s3="其他玩法：Box、iBox 与 Roll", p3="<strong>正字（Straight）</strong>只在号码顺序完全相同时才中奖。想包含其他排列：",
  ways=["<strong>Box（全包）</strong>：把所有排列各买一注，所以较贵（1234 每注 RM1 共 RM24），但每次中奖都拿全额奖金。", "<strong>iBox</strong>：一注（从 RM1 起）包含所有排列，任何排列都能中，但奖金按排列数平分。", "<strong>Roll（滚字）</strong>：其中一位变成 0–9，例如 12R4 包含 1204、1214 … 1294，共 10 个号码 RM10。"],
  pcap="一个号码有几种排列", pt=["数字", "例子", "排列"], prow=[("四个都不同", "1234", "24"), ("一对相同", "1123", "12"), ("两对相同", "1122", "6"), ("三个相同", "1112", "4")],
  pnote="各公司的玩法名称和最低注额略有不同，例如大马彩称为 B24/IB24。下注前请查看该公司的官方说明。",
  s4="真实的中奖机会", p4="10,000 个号码里有 23 个奖，所以一张 RM1 大字约有 <strong>1/435</strong> 的机会中任何奖，小字约 <strong>1/3,333</strong>。长期来看，每花 RM1 大约只回收 <strong>64–65 仙</strong>。请把万字当作有成本的娱乐，绝不是收入来源。",
  s5="开彩日期与成绩", p5="万能、多多和大马彩逢 <strong>星期三、六、日晚上7点</strong>开彩，另有公司宣布的特别开彩（通常在星期二）。豪龙 GD Lotto 与 9 Lotto 每晚开彩。晚上7点起，可在 <a href=\"{home}\">4D Malam Ini</a> 一页看齐所有公司的成绩，也可<a href=\"{check}\">查询任何号码</a>过去五年的中奖记录。",
  s6="谁可以玩与领奖", rules=["只有 <strong>21岁或以上的非穆斯林</strong>可以买票或领奖。", "只在各公司的合法投注站购买。向第三方或非法外围购买的票不会获得赔付，而且属违法行为。", "妥善保管彩票，领奖规则与期限请查看公司官方网页。", "先定好预算，不要追输，玩得不开心就停下来。"],
  s7="各公司玩法", s8="官方玩法说明", official="一切规则与奖金以公司官方网页为准。",
  opdesc={"M": "逢三、六、日 · 晚上7点", "T": "逢三、六、日 · 晚上7点", "D": "逢三、六、日 · 晚上7点"},
  op=dict(
    M=("万能 Magnum 4D 怎么玩", "万能 Magnum 4D：大字、小字、每 RM1 奖金与开彩日期简单说明，附万能官方玩法链接。",
       "万能 Magnum 4D 是马来西亚首家获准经营万字的私人公司万能的经典万字游戏。选 0000 到 9999 的号码，选大字或小字和注额即可。",
       ["大字包含全部 23 个中奖号码；小字只有头、二、三奖。", "每 RM1 奖金：大字 RM2,500 / 1,000 / 500，特别奖 RM180，安慰奖 RM60；小字 RM3,500 / 2,000 / 1,000。", "万能另有 4D Jackpot 等游戏，规则各不相同，请看万能官方网页。", "可在万能投注站提前购买之后几期的彩票。"]),
    T=("多多 Sports Toto 4D 怎么玩", "多多 Sports Toto 4D：大字与小字、每 RM1 奖金、Box 与 iBox 及开彩日期，附多多官方说明链接。",
       "多多 4D 的玩法与其他马来西亚万字相同：选 0000–9999，选大字或小字和注额。多多另有 4D Jackpot、5D、6D 与 Toto 等游戏，规则另计。",
       ["大字包含 23 个中奖号码；小字只有前三奖。", "每 RM1 奖金：大字 RM2,500 / 1,000 / 500，特别奖 RM180，安慰奖 RM60；小字 RM3,500 / 2,000 / 1,000。", "Box 与 iBox 可包含号码的所有排列，见主攻略的表格。", "4D Jackpot 的规则与奖金请看多多官方网页。"]),
    D=("大马彩 Da Ma Cai 1+3D 怎么玩", "大马彩 1+3D 说明：ABC（大字）与 A（小字）、入围奖、Box、iBox（IB24/IB12/IB6/IB4）与 Roll，每 RM1 奖金。",
       "大马彩的万字游戏叫 1+3D。注项用字母表示：<strong>ABC</strong> 是大字（23 个号码），<strong>A</strong> 是小字（只有头、二、三奖）。特别奖在大马彩叫 <strong>入围奖（Starter）</strong>。",
       ["正字最低 RM1。", "Box：B24 / B12 / B6 / B4 分别 RM24 / RM12 / RM6 / RM4，中奖拿全额奖金。", "iBox：IB24 / IB12 / IB6 / IB4 从 RM1 起；例如 IB24 大字头奖每 RM1 得 RM105。", "Roll 从 RM10 起；Lucky Pick（电脑选号）从 RM1 起。"]),
  ),
  checkbtn="查询万字号码", back="← 返回万字攻略", res="查看最新成绩", lnk="官方网页",
),
"ta": dict(
  home="முகப்பு", guide="4D வழிகாட்டி", title="4D விளையாடுவது எப்படி: Big, Small, Box",
  desc="மலேசியா 4D எளிய வழிகாட்டி: Big மற்றும் Small, ஒவ்வொரு RM1-க்கும் பரிசு, Box, iBox, Roll, வெல்லும் வாய்ப்பு, குலுக்கல் நாட்கள், முடிவுகளைச் சரிபார்ப்பது.",
  h1="மலேசியாவில் 4D விளையாடுவது எப்படி", sub="Big, Small, ஒவ்வொரு RM1-க்கான பரிசு, Box, iBox மற்றும் உண்மையான வாய்ப்புகள் — எளிமையாக.",
  toc=[("pick", "எண் தேர்வு"), ("bigsmall", "Big / Small"), ("ways", "Box & iBox"), ("odds", "வாய்ப்பு"), ("days", "குலுக்கல் நாட்கள்"), ("rules", "விதிகள்")],
  s1="4 இலக்க எண்ணைத் தேர்ந்தெடுங்கள்", p1="<strong>0000</strong> முதல் <strong>9999</strong> வரை எந்த எண்ணும் — மொத்தம் 10,000 எண்கள். பலர் பிறந்த நாள், வாகன எண் அல்லது <a href=\"{dict}\">4D அகராதி 万字图</a>-இல் தேடிய கனவைப் பயன்படுத்துகிறார்கள். ஒவ்வொரு குலுக்கலிலும் ஒவ்வொரு எண்ணுக்கும் ஒரே வாய்ப்புதான்.",
  s2="Big அல்லது Small தேர்வு", p2="ஒவ்வொரு குலுக்கலிலும் 23 வெற்றி எண்கள்: முதல், இரண்டாம், மூன்றாம் பரிசு, 10 சிறப்பு (Starter) மற்றும் 10 ஆறுதல் பரிசுகள்.",
  big="<strong>Big</strong> — 23 எண்களிலும் வெல்லலாம். முதன்மைப் பரிசு குறைவு, வெல்லும் வழிகள் அதிகம்.", small="<strong>Small</strong> — முதல் 3 பரிசுகளில் மட்டும். முதன்மைப் பரிசு அதிகம், வழிகள் குறைவு.",
  tcap="ஒவ்வொரு RM1 பந்தயத்துக்கான பரிசு", tprize="பரிசு", tbig="Big", tsmall="Small", rows=["முதல் பரிசு", "இரண்டாம் பரிசு", "மூன்றாம் பரிசு", "சிறப்பு / Starter (10)", "ஆறுதல் (10)"],
  ex="<strong>உதாரணம்:</strong> 1234 மீது RM2 Big. 1234 இரண்டாம் பரிசாக வந்தால் 2 × RM1,000 = <strong>RM2,000</strong>. சிறப்புப் பரிசு எண்ணாக வந்தால் 2 × RM180 = <strong>RM360</strong>. அதே எண்ணில் Small என்றால் சிறப்புப் பரிசுக்கு ஒன்றும் கிடைக்காது.",
  s3="மற்ற வழிகள்: Box, iBox, Roll", p3="<strong>Straight</strong> பந்தயம் உங்கள் சரியான வரிசையில் இலக்கங்கள் வந்தால் மட்டுமே வெல்லும். மற்ற வரிசைகளையும் சேர்க்க:",
  ways=["<strong>Box</strong> — ஒவ்வொரு வரிசையையும் தனிப் பந்தயமாக வாங்கும்; செலவு அதிகம் (1234 க்கு RM1 வீதம் RM24) ஆனால் முழுப் பரிசு கிடைக்கும்.", "<strong>iBox</strong> — ஒரே பந்தயத்தில் (RM1 முதல்) எல்லா வரிசைகளும்; எந்த வரிசை வந்தாலும் வெல்லலாம், ஆனால் பரிசு வரிசைகளின் எண்ணிக்கையால் பிரிக்கப்படும்.", "<strong>Roll</strong> — ஒரு இடம் 0–9 ஆகும், எ.கா. 12R4 = 1204, 1214 … 1294: 10 எண்கள் RM10."],
  pcap="ஒரு எண்ணுக்கு எத்தனை வரிசைகள்", pt=["இலக்கங்கள்", "உதாரணம்", "வரிசைகள்"], prow=[("எல்லாம் வேறு", "1234", "24"), ("ஒரு ஜோடி", "1123", "12"), ("இரண்டு ஜோடி", "1122", "6"), ("மூன்று ஒன்றே", "1112", "4")],
  pnote="பெயர்களும் குறைந்தபட்ச பந்தயமும் நிறுவனத்துக்கு நிறுவனம் சற்று மாறுபடும் — உதா. Da Ma Cai இவற்றை B24/IB24 என்கிறது. விளையாடும் முன் நிறுவனத்தின் அதிகாரப்பூர்வ பக்கத்தைப் பாருங்கள்.",
  s4="உங்கள் உண்மையான வாய்ப்பு", p4="10,000 எண்களில் 23 பரிசுகள் — ஒரு RM1 Big சீட்டுக்கு ஏதேனும் பரிசு வெல்லும் வாய்ப்பு சுமார் <strong>435-இல் 1</strong>, Small-க்கு <strong>3,333-இல் 1</strong>. நீண்ட காலத்தில் ஒவ்வொரு RM1-க்கும் சுமார் <strong>64–65 சென்</strong> மட்டுமே திரும்பக் கிடைக்கும். 4D-ஐ செலவுள்ள பொழுதுபோக்காகக் கருதுங்கள், வருமானமாக அல்ல.",
  s5="குலுக்கல் நாட்களும் முடிவுகளும்", p5="Magnum, Sports Toto, Da Ma Cai ஆகியவை <strong>புதன், சனி, ஞாயிறு இரவு 7 மணிக்கு</strong> குலுக்கல் நடத்துகின்றன; அறிவிக்கப்படும் சிறப்புக் குலுக்கல்களும் உண்டு (பெரும்பாலும் செவ்வாய்). GD Lotto, 9 Lotto தினமும் இரவில். இரவு 7 மணி முதல் <a href=\"{home}\">4D Malam Ini</a>-இல் எல்லா நிறுவனங்களின் முடிவுகளும் ஒரே பலகையில்; <a href=\"{check}\">எந்த எண்ணையும்</a> ஐந்து ஆண்டு பதிவுகளுடன் சரிபார்க்கலாம்.",
  s6="யார் விளையாடலாம், பரிசு கோருதல்", rules=["<strong>21 வயதுக்கு மேற்பட்ட முஸ்லிம் அல்லாதவர்கள்</strong> மட்டுமே சீட்டு வாங்கவோ பரிசு கோரவோ முடியும்.", "நிறுவனங்களின் உரிமம் பெற்ற கடைகளில் மட்டுமே வாங்குங்கள். மூன்றாம் தரப்பு அல்லது சட்டவிரோத புக்கிகளின் சீட்டுகளுக்குப் பணம் கிடைக்காது; வாங்குவது குற்றம்.", "சீட்டைப் பத்திரமாக வைத்திருங்கள்; பரிசு கோரும் விதிகளையும் கால அவகாசத்தையும் அதிகாரப்பூர்வ பக்கத்தில் பாருங்கள்.", "பட்ஜெட் வையுங்கள், இழப்பைத் துரத்தாதீர்கள், மகிழ்ச்சி இல்லையெனில் இடைவெளி எடுங்கள்."],
  s7="நிறுவன வாரியான வழிகாட்டி", s8="அதிகாரப்பூர்வ விளையாட்டு வழிகாட்டிகள்", official="நிறுவனத்தின் அதிகாரப்பூர்வ பக்கத்தில் உள்ள விதிகளும் பரிசுத் தொகைகளுமே இறுதியானவை.",
  opdesc={"M": "புதன், சனி, ஞாயிறு · இரவு 7", "T": "புதன், சனி, ஞாயிறு · இரவு 7", "D": "புதன், சனி, ஞாயிறு · இரவு 7"},
  op=dict(
    M=("Magnum 4D விளையாடுவது எப்படி", "Magnum 4D: Big, Small, ஒவ்வொரு RM1-க்கான பரிசு, குலுக்கல் நாட்கள் — Magnum அதிகாரப்பூர்வ பக்க இணைப்புடன்.",
       "Magnum 4D என்பது மலேசியாவில் 4D நடத்த உரிமம் பெற்ற முதல் தனியார் நிறுவனமான Magnum-இன் பாரம்பரிய 4D விளையாட்டு. 0000–9999 இல் ஒரு எண், Big அல்லது Small, தொகை — அவ்வளவுதான்.",
       ["Big 23 வெற்றி எண்களையும் உள்ளடக்கும்; Small முதல் 3 பரிசுகள் மட்டும்.", "RM1-க்கான பரிசு: Big RM2,500 / 1,000 / 500, சிறப்பு RM180, ஆறுதல் RM60. Small RM3,500 / 2,000 / 1,000.", "Magnum-இல் 4D Jackpot போன்ற பிற விளையாட்டுகளும் உண்டு — விதிகள் அதிகாரப்பூர்வ பக்கத்தில்.", "வரவிருக்கும் குலுக்கல்களுக்கு Magnum கடைகளில் முன்கூட்டியே சீட்டு வாங்கலாம்."]),
    T=("Sports Toto 4D விளையாடுவது எப்படி", "Sports Toto 4D: Big, Small, RM1-க்கான பரிசு, Box, iBox, குலுக்கல் நாட்கள் — Sports Toto அதிகாரப்பூர்வ வழிகாட்டி இணைப்புடன்.",
       "Sports Toto 4D மற்ற மலேசிய 4D விளையாட்டுகள் போன்றதே: 0000–9999 தேர்ந்தெடுத்து, Big அல்லது Small மற்றும் தொகை. Sports Toto-வில் 4D Jackpot, 5D, 6D, Toto போன்றவை தனி விதிகளுடன் உள்ளன.",
       ["Big 23 வெற்றி எண்கள்; Small முதல் 3 மட்டும்.", "RM1-க்கான பரிசு: Big RM2,500 / 1,000 / 500, சிறப்பு RM180, ஆறுதல் RM60. Small RM3,500 / 2,000 / 1,000.", "Box, iBox உங்கள் இலக்கங்களின் எல்லா வரிசைகளையும் உள்ளடக்கும் — முதன்மை வழிகாட்டியின் அட்டவணையைப் பாருங்கள்.", "4D Jackpot விதிகள் Sports Toto அதிகாரப்பூர்வ பக்கத்தில்."]),
    D=("Da Ma Cai 1+3D விளையாடுவது எப்படி", "Da Ma Cai 1+3D: ABC (Big), A (Small), Starter பரிசு, Box, iBox (IB24/IB12/IB6/IB4), Roll, RM1-க்கான பரிசு.",
       "Da Ma Cai-யின் 4D விளையாட்டின் பெயர் 1+3D. பந்தய வகைகள் எழுத்துகளால்: <strong>ABC</strong> = Big (23 எண்கள்), <strong>A</strong> = Small (முதல் 3 மட்டும்). சிறப்புப் பரிசு இங்கு <strong>Starter</strong> எனப்படும்.",
       ["Straight பந்தயம் குறைந்தது RM1.", "Box: B24 / B12 / B6 / B4 விலை RM24 / RM12 / RM6 / RM4, முழுப் பரிசு.", "iBox: IB24 / IB12 / IB6 / IB4 RM1 முதல்; எ.கா. IB24 Big முதல் பரிசு RM1-க்கு RM105.", "Roll RM10 முதல்; Lucky Pick (சீரற்ற எண்) RM1 முதல்."]),
  ),
  checkbtn="4D எண்ணைச் சரிபார்", back="← 4D வழிகாட்டிக்குத் திரும்ப", res="சமீபத்திய முடிவுகள்", lnk="அதிகாரப்பூர்வ பக்கம்",
),
}

PRIZES = [("2,500", "3,500"), ("1,000", "2,000"), ("500", "1,000"), ("180", "—"), ("60", "—")]
FOOT = {
 "en": "Unofficial guide for reference. Rules and prizes on the company's official page take priority. 21+ · Non-Muslims only · Play responsibly.",
 "ms": "Panduan tidak rasmi untuk rujukan. Peraturan dan hadiah di halaman rasmi syarikat diutamakan. 21+ · Bukan Islam sahaja · Main secara bertanggungjawab.",
 "zh": "非官方参考攻略，一切以公司官方网页为准。仅限21岁或以上非穆斯林 · 理性投注。",
 "ta": "குறிப்புக்கான அதிகாரப்பூர்வமற்ற வழிகாட்டி. நிறுவன அதிகாரப்பூர்வ பக்கமே இறுதி. 21+ · முஸ்லிம் அல்லாதவர்கள் மட்டும் · பொறுப்புடன் விளையாடுங்கள்.",
}


def build(site) -> None:
    """site: seo_pages.Site (already built, so site.css exists)."""
    import hashlib, shutil
    from pathlib import Path
    (site.out / "assets").mkdir(exist_ok=True)
    font = Path(__file__).with_name("brand") / "fonts" / "jakarta-latin.woff2"
    font_url, preload = "", ""
    if font.exists():
        fname = "assets/jakarta." + hashlib.sha256(font.read_bytes()).hexdigest()[:8] + ".woff2"
        shutil.copy2(font, site.out / fname)
        font_url = site.u(fname)
        preload = f'<link rel="preload" href="{font_url}" as="font" type="font/woff2" crossorigin>'
    css = CSS.replace("__FONT__", font_url or "about:blank")
    css_name = "assets/g." + hashlib.sha256(css.encode()).hexdigest()[:8] + ".css"
    (site.out / css_name).write_text(css)
    cssl = preload + f'<link rel="stylesheet" href="{site.u(css_name)}">'
    logo = lambda k: site.u(f"img/op/{k.lower()}{'-n' if k in 'TD' else ''}.webp?v=3")  # light-text versions on dark cards

    def path(lang, sub=""):
        return LANGS[lang][1] + "guide/" + sub

    def alts(sub=""):
        h = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l, sub)}">' for l in LANGS)
        return h + f'<link rel="alternate" hreflang="x-default" href="{site.site}{path("en", sub)}">'

    def top(cur, crumbs_html, sub=""):
        names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
        bar = '<nav class="lng" aria-label="Language">' + "".join(
            f'<a href="{site.u(path(l, sub))}" hreflang="{LANGS[l][0]}" lang="{LANGS[l][0]}"' + (' aria-current="page"' if l == cur else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        return f'<div class="top">{crumbs_html}{bar}</div>'

    def foot(lang):
        x = T[lang]
        home = site.u(LANGS[lang][1])
        return (f'<footer>{esc(FOOT[lang])}<br><a href="{home}">{esc(x["res"])}</a> · <a href="{site.u(path(lang))}">{esc(x["guide"])}</a> · '
                f'<a href="{site.u("keputusan/")}">Arkib · Archive</a> · <a href="{site.u("4d/")}">万字图</a></footer>')

    for lang, x in T.items():
        home = site.u(LANGS[lang][1])
        links = {"home": home, "check": home + "?tab=check", "dict": home + "?tab=dict"}
        hl = LANGS[lang][0]
        bc, bld = site.crumbs([(x["home"], LANGS[lang][1]), (x["guide"], None)])
        table = (f'<div class="tbl"><table><caption>{esc(x["tcap"])}</caption>'
                 f'<thead><tr><th scope="col">{esc(x["tprize"])}</th><th scope="col" class="n">{esc(x["tbig"])}</th><th scope="col" class="n">{esc(x["tsmall"])}</th></tr></thead><tbody>'
                 + "".join(f'<tr><th scope="row">{esc(r)}</th><td class="n{" big" if i == 0 else ""}">RM{b}</td><td class="n{" big" if i == 0 else ""}{" na" if s_ == "—" else ""}">{("RM" + s_) if s_ != "—" else "—"}</td></tr>'
                           for i, (r, (b, s_)) in enumerate(zip(x["rows"], PRIZES)))
                 + "</tbody></table></div>")
        perm = (f'<div class="tbl"><table><caption>{esc(x["pcap"])}</caption><thead><tr>'
                + "".join(f'<th scope="col"{" class=\"n\"" if k == 2 else ""}>{esc(h)}</th>' for k, h in enumerate(x["pt"])) + "</tr></thead><tbody>"
                + "".join(f'<tr><th scope="row">{esc(a)}</th><td class="mono">{b}</td><td class="n">{c}</td></tr>' for a, b, c in x["prow"]) + "</tbody></table></div>")
        duo = (f'<div class="duo"><div>{x["big"]}<span class="cnt">23 / 23</span></div><div>{x["small"]}<span class="cnt">3 / 23</span></div></div>')
        opg = '<div class="opg">' + "".join(
            f'<a href="{site.u(path(lang, slug + "/"))}" style="--c:{c}"><img src="{logo(k)}" width="40" height="40" alt="" loading="lazy"><span><b>{esc(name)}</b><span>{esc(x["opdesc"][k])}</span></span></a>'
            for slug, k, name, c, _ in OPS) + "</div>"
        ext = '<div class="ext">' + "".join(f'<a href="{u}" target="_blank" rel="noopener nofollow">{esc(name)} — {esc(x["lnk"])}</a>' for _, _, name, _, u in OPS) + "</div>"
        toc = '<nav class="toc" aria-label="Contents">' + "".join(f'<a href="#{i}"><b>{n + 1}</b>{esc(t_)}</a>' for n, (i, t_) in enumerate(x["toc"])) + "</nav>"
        sec = lambda i, n, ttl, inner: f'<section class="st" id="{i}" aria-labelledby="{i}-h"><h2 id="{i}-h"><i>{n}</i>{esc(ttl)}</h2>{inner}</section>'
        body = (top(lang, bc) + f'<article class="gd"><div class="hero"><span class="kick">{esc(x["guide"])}</span><h1>{esc(x["h1"])}<small>{esc(x["sub"])}</small></h1></div>{toc}'
                + sec("pick", 1, x["s1"], f'<p>{x["p1"].format(**links)}</p>')
                + sec("bigsmall", 2, x["s2"], f'<p>{x["p2"]}</p>{duo}{table}<p class="note">{x["ex"]}</p>')
                + sec("ways", 3, x["s3"], f'<p>{x["p3"]}</p><ul>' + "".join(f"<li>{w}</li>" for w in x["ways"]) + f'</ul>{perm}<p class="note">{x["pnote"]}</p>')
                + sec("odds", 4, x["s4"], f'<p>{x["p4"]}</p>')
                + sec("days", 5, x["s5"], f'<p>{x["p5"].format(**links)}</p>')
                + sec("rules", 6, x["s6"], "<ul>" + "".join(f"<li>{r}</li>" for r in x["rules"]) + "</ul>")
                + f'<section class="st"><h2 style="grid-template-columns:1fr">{esc(x["s7"])}</h2>{opg}</section>'
                + f'<section class="st"><h2 style="grid-template-columns:1fr">{esc(x["s8"])}</h2>{ext}<p class="note warn">{esc(x["official"])}</p></section>'
                + f'<div class="cta"><a class="p" href="{home}">{esc(x["res"])}</a><a class="s" href="{links["check"]}">{esc(x["checkbtn"])}</a></div></article>')
        art = {"@context": "https://schema.org", "@type": "Article", "headline": x["h1"], "inLanguage": hl, "description": x["desc"],
               "author": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site}, "publisher": {"@type": "Organization", "name": "4D Malam Ini"}}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"], body, lang=hl, ld=[bld, art], head=cssl + alts(), foot=foot(lang))

        for slug, k, name, c, url in OPS:
            ttl, dsc, intro, pts = x["op"][k]
            bc, bld = site.crumbs([(x["home"], LANGS[lang][1]), (x["guide"], path(lang)), (name, None)])
            body = (top(lang, bc, slug + "/") + f'<article class="gd"><div class="ophero" style="--c:{c}"><img src="{logo(k)}" width="56" height="56" alt="{esc(name)}"><h1>{esc(ttl)}<small>{esc(x["opdesc"][k])}</small></h1></div>'
                    f'<section class="st"><p>{intro}</p><ul>' + "".join(f"<li>{p}</li>" for p in pts) + f'</ul>{table}<p class="note warn">{esc(x["official"])}</p></section>'
                    f'<div class="cta"><a class="p" href="{url}" target="_blank" rel="noopener nofollow">{esc(name)} — {esc(x["lnk"])} ↗</a>'
                    f'<a class="s" href="{home}#rc-{k}">{esc(x["res"])}</a></div>'
                    f'<a class="back" href="{site.u(path(lang))}">{esc(x["back"])}</a></article>')
            art = {"@context": "https://schema.org", "@type": "Article", "headline": ttl, "inLanguage": hl, "description": dsc,
                   "author": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site}}
            site.page(path(lang, slug + "/"), ttl + " | 4D Malam Ini", dsc, body, lang=hl, ld=[bld, art], head=cssl + alts(slug + "/"), foot=foot(lang))
