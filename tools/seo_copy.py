"""SEO copy for the 4 language home pages: an intro + FAQ block, and the FAQPage JSON-LD built from the same text.
Edit the text here; build.py drops it into <!--SEO--> on each home page."""
import html as H
import json

META = {
    "en": ("4D Result Today: Magnum, Toto, DMC, GD | 4D Malam Ini",
           "Malaysia 4D results today: Magnum 4D, Sports Toto, Da Ma Cai 1+3D, GD Lotto and 9 Lotto, updated live from 7pm. Check any number against 5 years of draws."),
    "ms": ("Keputusan 4D Hari Ini: Magnum, Toto, DMC | 4D Malam Ini",
           "Keputusan 4D hari ini: Magnum 4D, Sports Toto, Da Ma Cai 1+3D, GD Lotto dan 9 Lotto, dikemas kini dari 7 malam. Semak nombor anda dengan rekod 5 tahun."),
    "zh": ("今日万字成绩：万能、多多、大马彩、豪龙 | 4D Malam Ini",
           "今日马来西亚万字成绩：万能 Magnum 4D、多多 Sports Toto、大马彩 Da Ma Cai、豪龙 GD Lotto 与 9 Lotto，晚上7点起即时更新。查询号码5年中奖记录与万字图。"),
    "ta": ("இன்றைய 4D முடிவுகள்: Magnum, Toto, DMC | 4D Malam Ini",
           "இன்றைய மலேசியா 4D முடிவுகள்: Magnum 4D, Sports Toto, Da Ma Cai 1+3D, GD Lotto, 9 Lotto — இரவு 7 மணி முதல் புதுப்பிக்கப்படும். உங்கள் எண்ணை 5 ஆண்டு பதிவுகளுடன் சரிபாருங்கள்."),
}

H1 = {
    "en": "Malaysia 4D results today — Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto",
    "ms": "Keputusan 4D Malaysia hari ini — Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto",
    "zh": "今日马来西亚万字成绩 — 万能、多多、大马彩、豪龙、9 Lotto",
    "ta": "இன்றைய மலேசியா 4D முடிவுகள் — Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto",
}

# Each language: heading, intro paragraphs (HTML allowed: links), FAQ heading, FAQ [(q, a_html)]
COPY = {
"en": {
 "h": "4D results Malaysia: every draw, one page",
 "p": [
  '<strong>4D Malam Ini</strong> shows tonight\'s <strong>Magnum 4D</strong>, <strong>Sports Toto 4D</strong>, <strong>Da Ma Cai 1+3D</strong>, <strong>GD Lotto 4D</strong> and <strong>9 Lotto 4D</strong> results together, so you never have to open five websites. Results appear from about 7pm Malaysia time and are complete by around 8pm.',
  'Special and consolation prizes are sorted from smallest to biggest, which makes it quick to spot your number. Use the date buttons to go back to any past draw, or open the <a href="keputusan/">4D results archive</a> for every draw since 2021.',
  'Want to know if a number has ever won? <a href="?tab=check">Check a 4D number</a> against five years of draws, see which prize it won and when, or browse popular picks like <a href="4d/8888/">8888</a> and <a href="4d/1314/">1314</a>. The <a href="4d/">4D dictionary 万字图</a> explains what each number means, in English, Malay, Chinese and Tamil.',
 ],
 "fh": "Frequently asked questions",
 "faq": [
  ("What time are the 4D results out tonight?", "Magnum, Sports Toto and Da Ma Cai draw at 7pm on Wednesday, Saturday and Sunday, plus special draws announced by the operators. GD Lotto and 9 Lotto draw every evening. This page updates as the results come in, usually complete by 8pm."),
  ("How do I check if my 4D number won?", 'Type your 4-digit number in <a href="?tab=check">Check number</a>. You will see every win across all operators in the last five years, with the date and prize. Each number also has its own page, for example <a href="4d/0000/">4D 0000</a>.'),
  ("Why are special and consolation numbers sorted?", "Sorting them from small to big lets you scan for your number in seconds instead of reading every box. The 1st, 2nd and 3rd prizes stay in prize order."),
  ("What is the 4D dictionary (万字图)?", 'It is the traditional picture book that links each number from 0000 to 9999 to a meaning or object, used to turn dreams and events into numbers. Search it in any of the four languages in the <a href="?tab=dict">dictionary tab</a>.'),
  ("Are these the official results?", "No. 4D Malam Ini is an unofficial reference compiled from public results. Always confirm with the operator before claiming a prize. For non-Muslims aged 21 and above only. Please play responsibly."),
 ],
},
"ms": {
 "h": "Keputusan 4D Malaysia: semua cabutan, satu halaman",
 "p": [
  '<strong>4D Malam Ini</strong> memaparkan keputusan <strong>Magnum 4D</strong>, <strong>Sports Toto 4D</strong>, <strong>Da Ma Cai 1+3D</strong>, <strong>GD Lotto 4D</strong> dan <strong>9 Lotto 4D</strong> malam ini dalam satu tempat, jadi anda tidak perlu buka lima laman web. Keputusan keluar dari kira-kira jam 7 malam dan lengkap sekitar jam 8 malam.',
  'Nombor hadiah istimewa (special) dan saguhati (consolation) disusun dari kecil ke besar supaya nombor anda mudah dijumpai. Guna butang tarikh untuk melihat cabutan lepas, atau buka <a href="keputusan/">arkib keputusan 4D</a> untuk semua cabutan sejak 2021.',
  'Mahu tahu sama ada sesuatu nombor pernah menang? <a href="?tab=check">Semak nombor 4D</a> dengan rekod lima tahun, lihat hadiah dan tarikhnya, atau lihat nombor popular seperti <a href="4d/8888/">8888</a> dan <a href="4d/1314/">1314</a>. <a href="4d/">Kamus 4D 万字图</a> menerangkan maksud setiap nombor dalam bahasa Melayu, Inggeris, Cina dan Tamil.',
 ],
 "fh": "Soalan lazim",
 "faq": [
  ("Pukul berapa keputusan 4D keluar malam ini?", "Magnum, Sports Toto dan Da Ma Cai membuat cabutan jam 7 malam pada hari Rabu, Sabtu dan Ahad, serta cabutan khas yang diumumkan oleh syarikat. GD Lotto dan 9 Lotto membuat cabutan setiap malam. Halaman ini dikemas kini ketika keputusan keluar, biasanya lengkap sebelum jam 8 malam."),
  ("Bagaimana nak semak nombor 4D saya menang atau tidak?", 'Taip nombor 4 digit anda di <a href="?tab=check">Semak nombor</a>. Anda akan nampak semua kemenangan bagi semua syarikat dalam lima tahun lepas, berserta tarikh dan hadiah. Setiap nombor juga ada halaman sendiri, contohnya <a href="4d/0000/">4D 0000</a>.'),
  ("Kenapa nombor special dan consolation disusun?", "Susunan dari kecil ke besar membolehkan anda mencari nombor dalam beberapa saat. Hadiah pertama, kedua dan ketiga kekal mengikut susunan hadiah."),
  ("Apa itu kamus 4D (万字图)?", 'Buku gambar tradisional yang mengaitkan setiap nombor dari 0000 hingga 9999 dengan maksud atau objek, digunakan untuk menukar mimpi dan kejadian kepada nombor. Cari dalam mana-mana empat bahasa di <a href="?tab=dict">tab kamus</a>.'),
  ("Adakah ini keputusan rasmi?", "Tidak. 4D Malam Ini ialah rujukan tidak rasmi yang dikumpul daripada keputusan awam. Sentiasa sahkan dengan syarikat sebelum menuntut hadiah. Hanya untuk bukan Islam berumur 21 tahun ke atas. Main secara bertanggungjawab."),
 ],
},
"zh": {
 "h": "马来西亚万字成绩：所有开彩，一页看完",
 "p": [
  '<strong>4D Malam Ini</strong> 把今晚 <strong>万能 Magnum 4D</strong>、<strong>多多 Sports Toto</strong>、<strong>大马彩 Da Ma Cai 1+3D</strong> 、<strong>豪龙 GD Lotto</strong> 和 <strong>9 Lotto</strong> 的万字成绩放在同一页，不用再开五个网站。成绩约晚上7点开始公布，8点左右全部完整。',
  '特别奖（入围奖）和安慰奖号码由小到大排列，一眼就能找到你的号码。用日期按钮查看任何一期旧成绩，或打开<a href="keputusan/">万字成绩记录</a>，查看2021年以来的每一期。',
  '想知道某个号码有没有中过？<a href="?tab=check">查询万字号码</a>，对照5年开彩记录，看中过什么奖、哪一天中；也可以看看热门号码如 <a href="4d/8888/">8888</a>、<a href="4d/1314/">1314</a>。<a href="4d/">万字图 4D 字典</a>以中文、英文、马来文和淡米尔文解释每个号码的含义。',
 ],
 "fh": "常见问题",
 "faq": [
  ("今晚万字成绩几点出？", "万能、多多和大马彩逢星期三、六、日晚上7点开彩，另有公司宣布的特别开彩日。豪龙 GD Lotto 与 9 Lotto 每晚开彩。本页随成绩公布即时更新，一般8点前完整。"),
  ("怎样查我的万字号码有没有中？", '在<a href="?tab=check">查号码</a>输入4位数号码，即可看到过去5年所有公司的中奖记录、日期和奖项。每个号码也有独立页面，例如 <a href="4d/0000/">万字 0000</a>。'),
  ("为什么特别奖和安慰奖要排序？", "由小到大排列，几秒内就能找到号码，不用逐格看。头奖、二奖、三奖仍按奖项顺序显示。"),
  ("什么是万字图？", '万字图是传统的号码图册，把0000到9999每个号码对应到一个含义或物件，常用来把梦境和生活事件转成号码。可在<a href="?tab=dict">万字图页面</a>用四种语言搜索。'),
  ("这是官方成绩吗？", "不是。4D Malam Ini 是根据公开成绩整理的非官方参考，领奖前请向相关公司核实。仅限21岁或以上非穆斯林，请理性投注。"),
 ],
},
"ta": {
 "h": "மலேசியா 4D முடிவுகள்: எல்லா குலுக்கல்களும் ஒரே பக்கத்தில்",
 "p": [
  '<strong>4D Malam Ini</strong> இன்றிரவு <strong>Magnum 4D</strong>, <strong>Sports Toto 4D</strong>, <strong>Da Ma Cai 1+3D</strong>, <strong>GD Lotto 4D</strong>, <strong>9 Lotto 4D</strong> முடிவுகளை ஒரே இடத்தில் காட்டுகிறது; ஐந்து இணையதளங்களைத் திறக்க வேண்டியதில்லை. முடிவுகள் மலேசிய நேரம் இரவு சுமார் 7 மணிக்கு வரத் தொடங்கி, 8 மணிக்குள் முழுமையாகும்.',
  'சிறப்பு (special) மற்றும் ஆறுதல் (consolation) பரிசு எண்கள் சிறியதிலிருந்து பெரியது வரை வரிசைப்படுத்தப்பட்டுள்ளன, எனவே உங்கள் எண்ணை விரைவாகக் கண்டுபிடிக்கலாம். தேதி பொத்தான்கள் மூலம் பழைய குலுக்கல்களைப் பாருங்கள், அல்லது 2021 முதல் உள்ள <a href="keputusan/">4D முடிவு காப்பகத்தைத்</a> திறக்கவும்.',
  'ஒரு எண் எப்போதாவது வென்றதா என்று அறிய வேண்டுமா? ஐந்து ஆண்டு குலுக்கல்களுடன் <a href="?tab=check">4D எண்ணைச் சரிபாருங்கள்</a>, அல்லது <a href="4d/8888/">8888</a>, <a href="4d/1314/">1314</a> போன்ற பிரபல எண்களைப் பாருங்கள். <a href="4d/">4D அகராதி 万字图</a> ஒவ்வொரு எண்ணின் பொருளையும் தமிழ், மலாய், ஆங்கிலம், சீனம் ஆகிய மொழிகளில் விளக்குகிறது.',
 ],
 "fh": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
 "faq": [
  ("இன்றிரவு 4D முடிவுகள் எத்தனை மணிக்கு வரும்?", "Magnum, Sports Toto, Da Ma Cai ஆகியவை புதன், சனி, ஞாயிறு இரவு 7 மணிக்கும், நிறுவனங்கள் அறிவிக்கும் சிறப்பு நாட்களிலும் குலுக்கல் நடத்துகின்றன. GD Lotto, 9 Lotto தினமும் இரவில் குலுக்கல் நடத்துகின்றன. முடிவுகள் வரும்போதே இந்தப் பக்கம் புதுப்பிக்கப்படும்; பொதுவாக 8 மணிக்குள் முழுமையாகும்."),
  ("என் 4D எண் வென்றதா என்று எப்படிச் சரிபார்ப்பது?", '<a href="?tab=check">எண் சரிபார்ப்பு</a> பகுதியில் உங்கள் 4 இலக்க எண்ணைத் தட்டச்சு செய்யுங்கள். கடந்த ஐந்து ஆண்டுகளில் எல்லா நிறுவனங்களிலும் பெற்ற வெற்றிகள், தேதி மற்றும் பரிசுடன் காட்டப்படும். ஒவ்வொரு எண்ணுக்கும் தனிப் பக்கம் உண்டு, எ.கா. <a href="4d/0000/">4D 0000</a>.'),
  ("சிறப்பு, ஆறுதல் பரிசு எண்கள் ஏன் வரிசைப்படுத்தப்பட்டுள்ளன?", "சிறியதிலிருந்து பெரியது வரை வரிசைப்படுத்துவதால் உங்கள் எண்ணைச் சில நொடிகளில் கண்டுபிடிக்கலாம். முதல், இரண்டாம், மூன்றாம் பரிசுகள் பரிசு வரிசையிலேயே இருக்கும்."),
  ("4D அகராதி (万字图) என்றால் என்ன?", '0000 முதல் 9999 வரை ஒவ்வொரு எண்ணையும் ஒரு பொருள் அல்லது அர்த்தத்துடன் இணைக்கும் பாரம்பரிய படப் புத்தகம்; கனவுகளையும் நிகழ்வுகளையும் எண்களாக மாற்றப் பயன்படுகிறது. <a href="?tab=dict">அகராதி பகுதியில்</a> நான்கு மொழிகளிலும் தேடலாம்.'),
  ("இவை அதிகாரப்பூர்வ முடிவுகளா?", "இல்லை. 4D Malam Ini பொது முடிவுகளிலிருந்து தொகுக்கப்பட்ட அதிகாரப்பூர்வமற்ற குறிப்பு. பரிசு கோருவதற்கு முன் நிறுவனத்திடம் உறுதிப்படுத்துங்கள். 21 வயதுக்கு மேற்பட்ட முஸ்லிம் அல்லாதவர்களுக்கு மட்டும்; பொறுப்புடன் விளையாடுங்கள்."),
 ],
},
}


def block(lang: str) -> str:
    c = COPY[lang]
    faq = "".join(f'<details><summary>{H.escape(q)}</summary><p>{a}</p></details>' for q, a in c["faq"])
    return (f'<section class="seo" data-l="{lang}" aria-labelledby="seo-h"><h2 id="seo-h">{H.escape(c["h"])}</h2>'
            + "".join(f"<p>{p}</p>" for p in c["p"])
            + f'<h2>{H.escape(c["fh"])}</h2><div class="faq">{faq}</div></section>')


def _plain(s: str) -> str:
    import re
    return H.unescape(re.sub(r"<[^>]+>", "", s))


def faq_ld(lang: str) -> str:
    d = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": {"zh": "zh-Hans"}.get(lang, lang),
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in COPY[lang]["faq"]]}
    return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False, separators=(",", ":"))}</script>'
