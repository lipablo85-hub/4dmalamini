"""/privacy/, /terms/ and /contact/ in four languages.

E-E-A-T pages. Everything here is a statement of fact about how the site actually works:
no accounts, no payments, GA4 for aggregate usage, four localStorage keys that never leave
the device, Cloudflare Pages hosting. Nothing is asserted about a legal entity, because
there is nothing verifiable to assert.
"""
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}

# localStorage keys the app actually uses, described for a reader
STORE = {
 "en": [("Language choice", "Which of the four languages you picked."),
        ("Saved numbers", "The numbers you add to My numbers, so the board can highlight them."),
        ("Cached results", "A copy of the draw history, so the site opens fast on your next visit."),
        ("Dismissed notices", "Which one-off tips you have already closed.")],
 "ms": [("Pilihan bahasa", "Bahasa mana antara empat yang anda pilih."),
        ("Nombor disimpan", "Nombor yang anda tambah ke Nombor saya, supaya papan boleh menyerlahkannya."),
        ("Keputusan cache", "Salinan sejarah cabutan, supaya laman dibuka pantas pada lawatan berikutnya."),
        ("Notis ditutup", "Petua sekali sahaja yang sudah anda tutup.")],
 "zh": [("语言选择", "您选择的是四种语言中的哪一种。"),
        ("已保存号码", "您添加到「我的号码」的号码，以便成绩板为您标示。"),
        ("成绩缓存", "开奖记录的副本，让您下次打开网站时更快。"),
        ("已关闭的提示", "您已经关闭过的一次性提示。")],
 "ta": [("மொழித் தேர்வு", "நான்கு மொழிகளில் நீங்கள் தேர்ந்தெடுத்தது எது."),
        ("சேமித்த எண்கள்", "‘என் எண்கள்’ இல் நீங்கள் சேர்த்த எண்கள், பலகை அவற்றைக் காட்ட."),
        ("முடிவுகள் தேக்ககம்", "குலுக்கல் வரலாற்றின் நகல், அடுத்த முறை தளம் வேகமாகத் திறக்க."),
        ("மூடிய அறிவிப்புகள்", "நீங்கள் ஏற்கனவே மூடிய ஒருமுறை குறிப்புகள்.")],
}

T = {
 "en": dict(
  home="Home",
  pv=dict(crumb="Privacy", title="Privacy — What We Collect and What We Don't | 4D Malam Ini",
    desc="4D Malam Ini has no accounts, no sign-up and no payments. What stays on your device, what Google Analytics sees, and how to clear it.",
    h1="Privacy", sub="Privasi · 隐私 · தனியுரிமை",
    lead="There is no account to create, nothing to sign up for and no payment to make, so there is nothing here that identifies you.",
    secs=[("What we never ask for", "<p>No name, no email, no phone number, no address, no payment details. The site has no login and no sign-up form. Nothing you type into the number check is sent to us — the search runs in your own browser against results it has already downloaded.</p>"),
          ("What stays on your device", "<p>Four things are saved in your browser's local storage. They never leave your device and we cannot read them.</p>{store}<p>Clearing your browser data for this site removes all four. Nothing breaks: the site rebuilds them as you use it.</p>"),
          ("What our analytics sees", "<p>We use Google Analytics 4 to count how the site is used — which pages are opened, roughly which country a visit came from, and what kind of device it was. It is aggregate: we cannot see an individual person, and we never upload what you searched for.</p><p>Analytics loads only after the page is ready, so it never slows down a result you are waiting for. Google's own policy explains what it collects: <a href=\"https://policies.google.com/privacy\" rel=\"nofollow noopener\" target=\"_blank\">policies.google.com/privacy</a>. Blocking it in your browser does not affect any feature of this site.</p>"),
          ("Hosting logs", "<p>The site runs on Cloudflare Pages. Like any web host, it keeps short-term request logs — IP address, time, page, browser — to serve the page and to stop abuse. We do not use them to build any profile.</p>"),
          ("Cookies", "<p>Only Google Analytics sets cookies. There are no advertising cookies and no cross-site tracking.</p>"),
          ("Age", "<p>This site is for people aged 21 and above. It is not aimed at children and we do not knowingly collect anything from them.</p>"),
          ("Questions", "<p>Message us on Telegram — the link is in the footer and on the <a href=\"{contact}\">contact page</a>.</p>")]),
  tm=dict(crumb="Terms", title="Terms of Use — Unofficial Results, No Betting | 4D Malam Ini",
    desc="4D Malam Ini publishes unofficial 4D results for reference. We do not sell tickets or take bets. Confirm with the operator before claiming a prize.",
    h1="Terms of use", sub="Terma penggunaan · 使用条款 · பயன்பாட்டு விதிமுறைகள்",
    lead="Short version: the numbers here are a reference copy, not an official record, and this site has nothing to do with buying a ticket.",
    secs=[("The results are unofficial", "<p>We compile results from each operator's own published pages. Mistakes are possible — a transcription error, a page that changed after we read it, a draw an operator corrected later. Before you claim a prize, confirm the numbers with the operator. Their result is the one that counts, not ours. How we source and check them is set out in the <a href=\"{policy}\">data policy</a>.</p>"),
          ("We do not take bets", "<p>4D Malam Ini does not sell tickets, accept stakes, hold money, pay prizes or act for any operator. We are not affiliated with Magnum, Sports Toto, Da Ma Cai or any other company whose results we publish. If a site claims otherwise using our name, it is not us.</p>"),
          ("Who may use this site", "<p>4D is legal in Malaysia for non-Muslims aged 21 and above. Use this site only where it is lawful for you to do so.</p>"),
          ("No prediction, no advice", "<p>Nothing here predicts a draw. The statistics pages describe what has already happened. Each draw is independent: a number that has not appeared for a long time is not more likely to appear next. Treat everything on this site as information, not advice.</p>"),
          ("No warranty", "<p>The site is provided as it is. We do not promise it will be accurate, complete or available at any particular moment, and we are not liable for any loss arising from relying on it.</p>"),
          ("Names and logos", "<p>Operator names and logos belong to their owners. We use them only to identify whose result is whose.</p>"),
          ("Changes", "<p>These terms can change. The current version is always the one on this page.</p>")]),
  ct=dict(crumb="Contact", title="Contact 4D Malam Ini — Corrections & Questions | 4D Malam Ini",
    desc="Reach 4D Malam Ini on Telegram for a result correction, a question about our data, or anything else about the site. We reply in four languages.",
    h1="Contact us", sub="Hubungi kami · 联系我们 · எங்களைத் தொடர்பு கொள்ள",
    lead="One way in: Telegram. We read everything and reply in English, Bahasa Malaysia, 中文 or தமிழ்.",
    tg="Message us on Telegram",
    what="What to write about",
    items=[("A wrong result", "Tell us the date and the company. We check it against the operator's own page and fix it, usually the same day. How corrections work is in the <a href=\"{policy}\">data policy</a>."),
           ("A missing draw", "If a date shows no result for a company that should have drawn, send us the date."),
           ("Where a number came from", "Ask about any figure on the site and we will point you at its source."),
           ("Anything else", "Suggestions, problems with the site, or a question we have not thought of.")],
    nb="What we cannot help with",
    cant=["We cannot pay a prize or confirm a winning ticket — only the operator can do that.",
          "We do not sell tickets or take bets.",
          "We cannot tell you what will be drawn. Nobody can."],
    who="Who runs this", whop="4D Malam Ini is an independent results site, published in English, Bahasa Malaysia, 中文 and தமிழ். It is not operated by, or affiliated with, any 4D company."),
 ),
 "ms": dict(
  home="Utama",
  pv=dict(crumb="Privasi", title="Privasi — Apa Yang Kami Kumpul dan Tidak | 4D Malam Ini",
    desc="4D Malam Ini tiada akaun, tiada pendaftaran dan tiada pembayaran. Apa yang kekal pada peranti anda, apa yang dilihat Google Analytics, dan cara membersihkannya.",
    h1="Privasi", sub="Privacy · 隐私 · தனியுரிமை",
    lead="Tiada akaun untuk dibuka, tiada pendaftaran dan tiada pembayaran, jadi tiada apa-apa di sini yang mengenal pasti anda.",
    secs=[("Apa yang kami tidak pernah minta", "<p>Tiada nama, e-mel, nombor telefon, alamat atau butiran pembayaran. Laman ini tiada log masuk dan tiada borang pendaftaran. Apa yang anda taip dalam semakan nombor tidak dihantar kepada kami — carian berjalan dalam pelayar anda sendiri terhadap keputusan yang sudah dimuat turun.</p>"),
          ("Apa yang kekal pada peranti anda", "<p>Empat perkara disimpan dalam storan setempat pelayar anda. Ia tidak pernah meninggalkan peranti anda dan kami tidak boleh membacanya.</p>{store}<p>Membersihkan data pelayar untuk laman ini membuang kesemuanya. Tiada apa-apa rosak: laman akan membinanya semula sambil anda guna.</p>"),
          ("Apa yang dilihat analitik kami", "<p>Kami guna Google Analytics 4 untuk mengira cara laman digunakan — halaman mana dibuka, lebih kurang dari negara mana lawatan datang, dan jenis peranti apa. Ia agregat: kami tidak dapat melihat individu, dan kami tidak pernah memuat naik apa yang anda cari.</p><p>Analitik dimuatkan hanya selepas halaman siap, jadi ia tidak pernah melambatkan keputusan yang anda tunggu. Dasar Google sendiri menerangkan apa yang dikumpul: <a href=\"https://policies.google.com/privacy\" rel=\"nofollow noopener\" target=\"_blank\">policies.google.com/privacy</a>. Menyekatnya dalam pelayar anda tidak menjejaskan mana-mana ciri laman ini.</p>"),
          ("Log pengehosan", "<p>Laman ini berjalan di Cloudflare Pages. Seperti mana-mana hos web, ia menyimpan log permintaan jangka pendek — alamat IP, masa, halaman, pelayar — untuk menyajikan halaman dan menghalang penyalahgunaan. Kami tidak menggunakannya untuk membina sebarang profil.</p>"),
          ("Kuki", "<p>Hanya Google Analytics menetapkan kuki. Tiada kuki pengiklanan dan tiada penjejakan merentas laman.</p>"),
          ("Umur", "<p>Laman ini untuk mereka berumur 21 tahun ke atas. Ia bukan untuk kanak-kanak dan kami tidak mengumpul apa-apa daripada mereka dengan sengaja.</p>"),
          ("Soalan", "<p>Hubungi kami di Telegram — pautannya ada di pengaki dan di <a href=\"{contact}\">halaman hubungi</a>.</p>")]),
  tm=dict(crumb="Terma", title="Terma Penggunaan — Keputusan Tidak Rasmi | 4D Malam Ini",
    desc="4D Malam Ini menerbitkan keputusan 4D tidak rasmi untuk rujukan. Kami tidak menjual tiket atau menerima taruhan. Sahkan dengan syarikat sebelum menuntut hadiah.",
    h1="Terma penggunaan", sub="Terms of use · 使用条款 · பயன்பாட்டு விதிமுறைகள்",
    lead="Versi ringkas: nombor di sini ialah salinan rujukan, bukan rekod rasmi, dan laman ini tiada kaitan dengan membeli tiket.",
    secs=[("Keputusan ini tidak rasmi", "<p>Kami mengumpul keputusan daripada halaman terbitan setiap syarikat. Kesilapan mungkin berlaku — salah salin, halaman yang berubah selepas kami membacanya, atau cabutan yang syarikat betulkan kemudian. Sebelum menuntut hadiah, sahkan nombor dengan syarikat. Keputusan merekalah yang sah, bukan kami. Cara kami mendapatkan dan menyemaknya ada dalam <a href=\"{policy}\">dasar data</a>.</p>"),
          ("Kami tidak menerima taruhan", "<p>4D Malam Ini tidak menjual tiket, menerima pertaruhan, memegang wang, membayar hadiah atau bertindak bagi pihak mana-mana syarikat. Kami tiada gabungan dengan Magnum, Sports Toto, Da Ma Cai atau mana-mana syarikat lain yang keputusannya kami terbitkan. Jika ada laman mendakwa sebaliknya menggunakan nama kami, itu bukan kami.</p>"),
          ("Siapa boleh guna laman ini", "<p>4D adalah sah di Malaysia untuk bukan Islam berumur 21 tahun ke atas. Guna laman ini hanya di mana ia sah untuk anda.</p>"),
          ("Tiada ramalan, tiada nasihat", "<p>Tiada apa-apa di sini meramal cabutan. Halaman statistik menerangkan apa yang sudah berlaku. Setiap cabutan adalah bebas: nombor yang lama tidak keluar bukan lebih berkemungkinan keluar seterusnya. Anggap semua di laman ini sebagai maklumat, bukan nasihat.</p>"),
          ("Tiada jaminan", "<p>Laman ini disediakan sebagaimana adanya. Kami tidak menjanjikan ia tepat, lengkap atau tersedia pada bila-bila masa tertentu, dan kami tidak bertanggungjawab atas sebarang kerugian akibat bergantung kepadanya.</p>"),
          ("Nama dan logo", "<p>Nama dan logo syarikat adalah milik pemiliknya. Kami menggunakannya hanya untuk menandakan keputusan siapa.</p>"),
          ("Perubahan", "<p>Terma ini boleh berubah. Versi semasa sentiasa yang ada di halaman ini.</p>")]),
  ct=dict(crumb="Hubungi", title="Hubungi 4D Malam Ini — Pembetulan & Soalan | 4D Malam Ini",
    desc="Hubungi 4D Malam Ini di Telegram untuk pembetulan keputusan, soalan tentang data kami, atau apa-apa tentang laman ini. Kami membalas dalam empat bahasa.",
    h1="Hubungi kami", sub="Contact us · 联系我们 · எங்களைத் தொடர்பு கொள்ள",
    lead="Satu saluran: Telegram. Kami baca semuanya dan membalas dalam Bahasa Malaysia, English, 中文 atau தமிழ்.",
    tg="Hubungi kami di Telegram",
    what="Apa yang boleh ditulis",
    items=[("Keputusan salah", "Beritahu kami tarikh dan syarikatnya. Kami semak dengan halaman syarikat itu sendiri dan betulkan, biasanya pada hari yang sama. Cara pembetulan dijelaskan dalam <a href=\"{policy}\">dasar data</a>."),
           ("Cabutan hilang", "Jika sesuatu tarikh tiada keputusan untuk syarikat yang sepatutnya mencabut, hantar tarikhnya kepada kami."),
           ("Dari mana nombor itu datang", "Tanya tentang mana-mana angka di laman ini dan kami akan tunjukkan sumbernya."),
           ("Apa-apa lagi", "Cadangan, masalah dengan laman, atau soalan yang kami belum terfikir.")],
    nb="Apa yang kami tidak boleh bantu",
    cant=["Kami tidak boleh membayar hadiah atau mengesahkan tiket menang — hanya syarikat boleh.",
          "Kami tidak menjual tiket atau menerima taruhan.",
          "Kami tidak boleh memberitahu apa yang akan dicabut. Tiada siapa boleh."],
    who="Siapa kami", whop="4D Malam Ini ialah laman keputusan bebas, diterbitkan dalam Bahasa Malaysia, English, 中文 dan தமிழ். Ia tidak dikendalikan oleh, atau bergabung dengan, mana-mana syarikat 4D."),
 ),
 "zh": dict(
  home="首页",
  pv=dict(crumb="隐私", title="隐私 — 我们收集什么、不收集什么 | 4D Malam Ini",
    desc="4D Malam Ini 没有账号、无需注册、不涉及付款。哪些数据留在您的设备上、Google Analytics 看到什么，以及如何清除。",
    h1="隐私", sub="Privacy · Privasi · தனியுரிமை",
    lead="没有账号可开、没有注册、没有付款，所以这里没有任何能识别您身份的信息。",
    secs=[("我们从不索取的信息", "<p>不要姓名、电邮、电话号码、地址或付款资料。本站没有登录，也没有注册表格。您在号码查询中输入的内容不会发送给我们 — 搜索在您自己的浏览器中、针对已下载的成绩进行。</p>"),
          ("留在您设备上的数据", "<p>有四项内容保存在您浏览器的本地存储中。它们从不离开您的设备，我们也无法读取。</p>{store}<p>清除本站的浏览器数据会一并删除这四项。不会出问题：您继续使用时网站会重新建立。</p>"),
          ("我们的分析工具看到什么", "<p>我们使用 Google Analytics 4 统计网站的使用情况 — 哪些页面被打开、访问大致来自哪个国家、使用什么设备。这是汇总数据：我们看不到具体个人，也从不上传您查询过的内容。</p><p>分析脚本只在页面就绪后才加载，因此绝不会拖慢您正在等待的成绩。Google 自己的政策说明了它收集什么：<a href=\"https://policies.google.com/privacy\" rel=\"nofollow noopener\" target=\"_blank\">policies.google.com/privacy</a>。在浏览器中屏蔽它不会影响本站任何功能。</p>"),
          ("主机日志", "<p>本站运行于 Cloudflare Pages。与任何网站主机一样，它会保留短期请求日志 — IP 地址、时间、页面、浏览器 — 用于提供页面和防止滥用。我们不会用它建立任何用户画像。</p>"),
          ("Cookie", "<p>只有 Google Analytics 会设置 cookie。没有广告 cookie，也没有跨站追踪。</p>"),
          ("年龄", "<p>本站面向 21 岁及以上人士，并非针对儿童，我们也不会在知情下收集儿童的任何信息。</p>"),
          ("有疑问", "<p>请通过 Telegram 联系我们 — 链接在页脚和<a href=\"{contact}\">联系页面</a>。</p>")]),
  tm=dict(crumb="条款", title="使用条款 — 非官方成绩、不接受投注 | 4D Malam Ini",
    desc="4D Malam Ini 发布非官方万字成绩供参考。我们不卖彩票、不接受投注。兑奖前请向公司核实。",
    h1="使用条款", sub="Terms of use · Terma penggunaan · பயன்பாட்டு விதிமுறைகள்",
    lead="简短版本：这里的号码是参考副本，不是官方记录，本站与购买彩票毫无关系。",
    secs=[("成绩属非官方", "<p>我们从各公司自己公布的页面整理成绩。可能出错 — 抄录失误、我们读取后页面又变动、或公司事后更正的开奖。兑奖前请向公司核实号码。以他们的成绩为准，不是我们的。我们如何取得和核对，请见<a href=\"{policy}\">数据政策</a>。</p>"),
          ("我们不接受投注", "<p>4D Malam Ini 不卖彩票、不收注金、不经手资金、不派彩，也不代表任何公司。我们与万能、多多、大马彩或任何其他我们发布成绩的公司均无关联。若有网站冒用我们的名义声称相反，那不是我们。</p>"),
          ("谁可以使用本站", "<p>万字在马来西亚对 21 岁及以上的非穆斯林是合法的。请仅在对您合法的情况下使用本站。</p>"),
          ("没有预测，也不是建议", "<p>这里没有任何内容能预测开奖。统计页面描述的是已经发生的事。每一期开奖都是独立的：很久没开的号码，下一期并不会更可能开出。请把本站的一切视为信息，而非建议。</p>"),
          ("不作保证", "<p>本站按现状提供。我们不保证其准确、完整或在任何特定时刻可用，也不对因依赖本站而产生的任何损失负责。</p>"),
          ("名称与标志", "<p>公司名称和标志归其所有者所有。我们仅用于标示成绩属于哪一家。</p>"),
          ("变更", "<p>本条款可能变更。当前版本始终以本页面为准。</p>")]),
  ct=dict(crumb="联系", title="联系 4D Malam Ini — 更正与查询 | 4D Malam Ini",
    desc="通过 Telegram 联系 4D Malam Ini，报告成绩错误、询问数据来源或任何关于本站的问题。我们以四种语言回复。",
    h1="联系我们", sub="Contact us · Hubungi kami · எங்களைத் தொடர்பு கொள்ள",
    lead="一个渠道：Telegram。我们会阅读每一条讯息，并以中文、English、Bahasa Malaysia 或 தமிழ் 回复。",
    tg="通过 Telegram 联系我们",
    what="可以告诉我们什么",
    items=[("成绩有误", "请告知日期和公司。我们会对照该公司自己的页面核实并更正，通常当天完成。更正流程见<a href=\"{policy}\">数据政策</a>。"),
           ("缺少开奖", "若某个日期本该有某公司的成绩却是空白，请把日期发给我们。"),
           ("某个数字的来源", "本站任何数字都可以询问，我们会指出它的来源。"),
           ("其他任何事", "建议、网站问题，或我们没想到的疑问。")],
    nb="我们帮不上的事",
    cant=["我们无法派彩或确认中奖彩票 — 只有公司可以。",
          "我们不卖彩票、不接受投注。",
          "我们无法告诉您会开出什么。没有人可以。"],
    who="关于我们", whop="4D Malam Ini 是一个独立的成绩网站，以 English、Bahasa Malaysia、中文和 தமிழ் 发布。它不由任何万字公司运营，也与之无关联。"),
 ),
 "ta": dict(
  home="முகப்பு",
  pv=dict(crumb="தனியுரிமை", title="தனியுரிமை — நாங்கள் சேகரிப்பது, சேகரிக்காதது | 4D Malam Ini",
    desc="4D Malam Ini இல் கணக்கு இல்லை, பதிவு இல்லை, கட்டணம் இல்லை. உங்கள் சாதனத்தில் என்ன இருக்கிறது, Google Analytics என்ன பார்க்கிறது, எப்படி அழிப்பது.",
    h1="தனியுரிமை", sub="Privacy · Privasi · 隐私",
    lead="உருவாக்க கணக்கு இல்லை, பதிவு இல்லை, கட்டணம் இல்லை — எனவே உங்களை அடையாளம் காட்டும் எதுவும் இங்கு இல்லை.",
    secs=[("நாங்கள் ஒருபோதும் கேட்காதவை", "<p>பெயர், மின்னஞ்சல், தொலைபேசி எண், முகவரி, கட்டண விவரம் — எதுவும் இல்லை. இந்தத் தளத்தில் உள்நுழைவு இல்லை, பதிவுப் படிவமும் இல்லை. எண் சரிபார்ப்பில் நீங்கள் தட்டச்சு செய்வது எங்களுக்கு அனுப்பப்படுவதில்லை — தேடல் உங்கள் சொந்த உலாவியில், ஏற்கனவே பதிவிறக்கிய முடிவுகளுக்கு எதிராக நடக்கிறது.</p>"),
          ("உங்கள் சாதனத்தில் இருப்பவை", "<p>நான்கு விஷயங்கள் உங்கள் உலாவியின் லோக்கல் ஸ்டோரேஜில் சேமிக்கப்படுகின்றன. அவை உங்கள் சாதனத்தை விட்டு வெளியேறுவதில்லை, நாங்கள் அவற்றைப் படிக்கவும் முடியாது.</p>{store}<p>இந்தத் தளத்திற்கான உலாவித் தரவை அழித்தால் நான்கும் நீங்கும். எதுவும் பழுதாகாது: நீங்கள் பயன்படுத்தும்போது தளம் மீண்டும் உருவாக்கும்.</p>"),
          ("எங்கள் பகுப்பாய்வு பார்ப்பது", "<p>தளம் எப்படிப் பயன்படுத்தப்படுகிறது என்பதை எண்ண Google Analytics 4 பயன்படுத்துகிறோம் — எந்தப் பக்கங்கள் திறக்கப்படுகின்றன, வருகை தோராயமாக எந்த நாட்டிலிருந்து, என்ன வகை சாதனம். இது மொத்தத் தரவு: தனிநபரை எங்களால் பார்க்க முடியாது, நீங்கள் தேடியதை நாங்கள் ஒருபோதும் பதிவேற்றுவதில்லை.</p><p>பக்கம் தயாரான பிறகே பகுப்பாய்வு ஏற்றப்படுகிறது, எனவே நீங்கள் காத்திருக்கும் முடிவை அது தாமதப்படுத்துவதில்லை. Google இன் கொள்கை அது சேகரிப்பதை விளக்குகிறது: <a href=\"https://policies.google.com/privacy\" rel=\"nofollow noopener\" target=\"_blank\">policies.google.com/privacy</a>. உலாவியில் அதைத் தடுப்பது இந்தத் தளத்தின் எந்த அம்சத்தையும் பாதிக்காது.</p>"),
          ("ஹோஸ்டிங் பதிவுகள்", "<p>இந்தத் தளம் Cloudflare Pages இல் இயங்குகிறது. எந்த வலை ஹோஸ்டையும் போல, அது குறுகிய கால கோரிக்கைப் பதிவுகளை வைத்திருக்கிறது — IP முகவரி, நேரம், பக்கம், உலாவி — பக்கத்தை வழங்கவும் தவறான பயன்பாட்டைத் தடுக்கவும். எந்த சுயவிவரத்தையும் உருவாக்க நாங்கள் அவற்றைப் பயன்படுத்துவதில்லை.</p>"),
          ("குக்கீகள்", "<p>Google Analytics மட்டுமே குக்கீகளை அமைக்கிறது. விளம்பரக் குக்கீகள் இல்லை, தளங்களுக்கு இடையேயான கண்காணிப்பும் இல்லை.</p>"),
          ("வயது", "<p>இந்தத் தளம் 21 வயது மற்றும் அதற்கு மேற்பட்டவர்களுக்கானது. இது குழந்தைகளை இலக்காகக் கொண்டதல்ல, அவர்களிடமிருந்து எதையும் அறிந்தே சேகரிப்பதில்லை.</p>"),
          ("கேள்விகள்", "<p>Telegram இல் எங்களுக்குச் செய்தி அனுப்புங்கள் — இணைப்பு அடிக்குறிப்பிலும் <a href=\"{contact}\">தொடர்புப் பக்கத்திலும்</a> உள்ளது.</p>")]),
  tm=dict(crumb="விதிமுறைகள்", title="பயன்பாட்டு விதிமுறைகள் — அதிகாரப்பூர்வமற்ற முடிவுகள் | 4D Malam Ini",
    desc="4D Malam Ini அதிகாரப்பூர்வமற்ற 4D முடிவுகளை வெளியிடுகிறது. சீட்டு விற்பதில்லை, பந்தயம் ஏற்பதில்லை. பரிசு கோரும் முன் நிறுவனத்துடன் உறுதிப்படுத்தவும்.",
    h1="பயன்பாட்டு விதிமுறைகள்", sub="Terms of use · Terma penggunaan · 使用条款",
    lead="சுருக்கமாக: இங்குள்ள எண்கள் ஒரு குறிப்பு நகல், அதிகாரப்பூர்வப் பதிவு அல்ல — இந்தத் தளத்திற்கு சீட்டு வாங்குவதுடன் எந்தத் தொடர்பும் இல்லை.",
    secs=[("முடிவுகள் அதிகாரப்பூர்வமற்றவை", "<p>ஒவ்வொரு நிறுவனமும் வெளியிடும் பக்கங்களிலிருந்து முடிவுகளைத் தொகுக்கிறோம். தவறுகள் சாத்தியம் — நகலெடுப்புப் பிழை, நாங்கள் படித்த பிறகு மாறிய பக்கம், பின்னர் நிறுவனம் திருத்திய குலுக்கல். பரிசு கோரும் முன் எண்களை நிறுவனத்துடன் உறுதிப்படுத்துங்கள். அவர்களின் முடிவே செல்லுபடியாகும், எங்களுடையது அல்ல. நாங்கள் எப்படிப் பெறுகிறோம், சரிபார்க்கிறோம் என்பது <a href=\"{policy}\">தரவுக் கொள்கையில்</a> உள்ளது.</p>"),
          ("நாங்கள் பந்தயம் ஏற்பதில்லை", "<p>4D Malam Ini சீட்டு விற்பதில்லை, பணயம் ஏற்பதில்லை, பணம் வைத்திருப்பதில்லை, பரிசு வழங்குவதில்லை, எந்த நிறுவனத்திற்காகவும் செயல்படுவதில்லை. Magnum, Sports Toto, Da Ma Cai அல்லது நாங்கள் முடிவுகளை வெளியிடும் வேறு எந்த நிறுவனத்துடனும் எங்களுக்குத் தொடர்பு இல்லை. எங்கள் பெயரைப் பயன்படுத்தி வேறு ஏதேனும் தளம் மாறாகக் கூறினால், அது நாங்கள் அல்ல.</p>"),
          ("யார் பயன்படுத்தலாம்", "<p>மலேசியாவில் 21 வயதுக்கு மேற்பட்ட முஸ்லிம் அல்லாதவர்களுக்கு 4D சட்டப்பூர்வமானது. உங்களுக்குச் சட்டப்பூர்வமான இடத்தில் மட்டுமே இந்தத் தளத்தைப் பயன்படுத்துங்கள்.</p>"),
          ("முன்னறிவிப்பு இல்லை, ஆலோசனையும் இல்லை", "<p>இங்கு எதுவும் குலுக்கலை முன்னறிவிப்பதில்லை. புள்ளிவிவரப் பக்கங்கள் ஏற்கனவே நடந்ததை விவரிக்கின்றன. ஒவ்வொரு குலுக்கலும் தனித்தனி: நீண்ட நாட்களாக வராத எண் அடுத்து வர அதிக வாய்ப்பில்லை. இந்தத் தளத்தில் உள்ள அனைத்தையும் தகவலாகக் கருதுங்கள், ஆலோசனையாக அல்ல.</p>"),
          ("உத்தரவாதம் இல்லை", "<p>தளம் உள்ளபடியே வழங்கப்படுகிறது. அது துல்லியமானது, முழுமையானது அல்லது குறிப்பிட்ட நேரத்தில் கிடைக்கும் என்று நாங்கள் உறுதியளிக்கவில்லை; அதை நம்பியதால் ஏற்படும் இழப்புக்கு நாங்கள் பொறுப்பல்ல.</p>"),
          ("பெயர்களும் சின்னங்களும்", "<p>நிறுவனப் பெயர்களும் சின்னங்களும் அவற்றின் உரிமையாளர்களுக்குச் சொந்தமானவை. எந்த முடிவு யாருடையது என்பதைக் காட்டவே அவற்றைப் பயன்படுத்துகிறோம்.</p>"),
          ("மாற்றங்கள்", "<p>இந்த விதிமுறைகள் மாறலாம். தற்போதைய பதிப்பு எப்போதும் இந்தப் பக்கத்தில் உள்ளதே.</p>")]),
  ct=dict(crumb="தொடர்பு", title="4D Malam Ini தொடர்பு — திருத்தங்கள் & கேள்விகள் | 4D Malam Ini",
    desc="முடிவுத் திருத்தம், தரவு பற்றிய கேள்வி அல்லது தளம் பற்றிய எதற்கும் Telegram இல் 4D Malam Ini ஐத் தொடர்பு கொள்ளுங்கள். நான்கு மொழிகளில் பதிலளிக்கிறோம்.",
    h1="எங்களைத் தொடர்பு கொள்ள", sub="Contact us · Hubungi kami · 联系我们",
    lead="ஒரே வழி: Telegram. அனைத்தையும் படிக்கிறோம், தமிழ், English, Bahasa Malaysia அல்லது 中文 இல் பதிலளிக்கிறோம்.",
    tg="Telegram இல் எங்களுக்குச் செய்தி அனுப்புங்கள்",
    what="எதைப் பற்றி எழுதலாம்",
    items=[("தவறான முடிவு", "தேதியையும் நிறுவனத்தையும் சொல்லுங்கள். நிறுவனத்தின் சொந்தப் பக்கத்துடன் சரிபார்த்துத் திருத்துவோம், பொதுவாக அதே நாளில். திருத்த நடைமுறை <a href=\"{policy}\">தரவுக் கொள்கையில்</a> உள்ளது."),
           ("விடுபட்ட குலுக்கல்", "ஒரு நிறுவனம் குலுக்க வேண்டிய தேதியில் முடிவு காட்டப்படாவிட்டால், அந்தத் தேதியை அனுப்புங்கள்."),
           ("ஒரு எண் எங்கிருந்து வந்தது", "தளத்தில் உள்ள எந்த எண்ணைப் பற்றியும் கேளுங்கள், அதன் மூலத்தைக் காட்டுவோம்."),
           ("வேறு எதுவும்", "ஆலோசனைகள், தளத்தில் சிக்கல்கள், அல்லது நாங்கள் யோசிக்காத கேள்வி.")],
    nb="நாங்கள் உதவ முடியாதவை",
    cant=["பரிசு வழங்கவோ வென்ற சீட்டை உறுதிப்படுத்தவோ எங்களால் முடியாது — நிறுவனத்தால் மட்டுமே முடியும்.",
          "நாங்கள் சீட்டு விற்பதில்லை, பந்தயம் ஏற்பதில்லை.",
          "என்ன வரும் என்று சொல்ல எங்களால் முடியாது. யாராலும் முடியாது."],
    who="யார் நடத்துகிறார்கள்", whop="4D Malam Ini ஒரு சுயாதீன முடிவுகள் தளம், English, Bahasa Malaysia, 中文 மற்றும் தமிழில் வெளியிடப்படுகிறது. இது எந்த 4D நிறுவனத்தாலும் நடத்தப்படவில்லை, அதனுடன் தொடர்பும் இல்லை."),
 ),
}

CSS = """.lg{max-width:680px}
.lg .lead{font-size:16px;line-height:1.6;color:#C9D4EA;margin:10px 0 22px}
.lg h2{font-size:17px;margin:26px 0 8px}
.lg p{font-size:14.5px;line-height:1.65;color:#C9D4EA;margin:8px 0}
.lg a{color:#E9C46B}
.lg dl{display:grid!important;grid-template-columns:1fr!important;gap:8px;margin:12px 0 4px}
.lg dl>div{background:#0F1F3D;border:1px solid #233862;border-radius:13px;padding:10px 13px}
.lg dt{font-size:14px;font-weight:700;color:#F8F4E8}
.lg dd{margin:2px 0 0}
.lg dd{margin:2px 0 0;font-size:13px;color:#9FB0D3;line-height:1.5}
.lg ul.x{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:7px}
.lg ul.x li{position:relative;padding:9px 13px 9px 32px;background:#0C1A33;border:1px solid #1D3157;border-radius:12px;font-size:13.5px;color:#9FB0D3;line-height:1.5}
.lg ul.x li::before{content:"×";position:absolute;left:13px;top:8px;color:#FF8A8F;font-weight:700}
.lg .tgb{display:inline-flex;align-items:center;gap:9px;min-height:52px;padding:0 20px;border-radius:14px;background:#229ED9;color:#fff;
 text-decoration:none;font-weight:700;font-size:15px;margin:6px 0 4px}
.lg .tgb svg{flex:none}
.lg .who{margin-top:26px;padding:13px 15px;background:#0C1A33;border-left:3px solid #E9C46B;border-radius:0 12px 12px 0}
.lg .who b{display:block;font-size:14px;margin-bottom:4px}
.lg .who p{font-size:13.5px;margin:0;color:#9FB0D3}
.lg .xr{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.lg .xr a{flex:1 1 30%;min-height:46px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:#172A4D;
 color:#F8F4E8;text-decoration:none;font-size:13.5px;font-weight:700;text-align:center;padding:0 10px}"""

TG = ('<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.9 4.3 18.7 19.4c-.2 1-.9 1.3-1.7.8'
      'l-4.8-3.6-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.9 8.9-8c.4-.3-.1-.5-.6-.2L6.5 13.1l-4.7-1.5c-1-.3-1-1 .2-1.5L20.5 3c.9-.3 1.6.2 1.4 1.3Z"/></svg>')
TGURL = "https://t.me/ssgsales"


def build(site) -> None:
    import hashlib
    from seo_pages import d8
    css = "assets/lg." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / css).write_text(CSS)
    lastmod = d8(site.dates[-1]).isoformat()

    def shell(lang, pre, hl, key, slug, body, ld):
        x = T[lang][key]
        alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{LANGS[l][1]}{slug}/">' for l in LANGS) \
            + f'<link rel="alternate" hreflang="x-default" href="{site.site}{slug}/">'
        xr = "".join(f'<a href="{site.u(h)}">{esc(t)}</a>' for t, h in (
            (T[lang]["pv"]["crumb"], pre + "privacy/"), (T[lang]["tm"]["crumb"], pre + "terms/"),
            (T[lang]["ct"]["crumb"], pre + "contact/")) if not h.endswith(slug.split("/")[-1] + "/"))
        site.page(f"{pre}{slug}/", x["title"], x["desc"],
                  f'<div class="lg">{body}<div class="xr">{xr}</div></div>', hl, ld, lastmod,
                  head=f'<link rel="stylesheet" href="{site.u(css)}">' + alts)

    for lang, (hl, pre) in LANGS.items():
        L, policy, contact = T[lang], site.u("data-policy/"), site.u(pre + "contact/")
        org = {"@context": "https://schema.org", "@type": "Organization", "name": "4D Malam Ini",
               "url": site.site, "logo": site.site + "icon-512.png", "sameAs": [TGURL],
               "description": L["ct"]["whop"], "publishingPrinciples": site.site + "data-policy/",
               "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "url": TGURL,
                                "availableLanguage": ["en", "ms", "zh", "ta"]}}

        # ---- privacy ----
        x = L["pv"]
        store = "<dl>" + "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in STORE[lang]) + "</dl>"
        nav, bld = site.crumbs([(L["home"], pre), (x["crumb"], None)])
        secs = "".join(f"<h2>{esc(h)}</h2>" + p.replace("{store}", store).replace("{contact}", contact) for h, p in x["secs"])
        shell(lang, pre, hl, "pv", "privacy",
              f'{nav}<h1>{esc(x["h1"])}<small>{esc(x["sub"])}</small></h1><p class="lead">{esc(x["lead"])}</p>{secs}',
              [bld, org, {"@context": "https://schema.org", "@type": "WebPage", "name": x["h1"], "inLanguage": hl,
                          "url": site.site + f"{pre}privacy/", "description": x["desc"], "publisher": {"@id": site.site}}])

        # ---- terms ----
        x = L["tm"]
        nav, bld = site.crumbs([(L["home"], pre), (x["crumb"], None)])
        secs = "".join(f"<h2>{esc(h)}</h2>" + p.replace("{policy}", policy) for h, p in x["secs"])
        shell(lang, pre, hl, "tm", "terms",
              f'{nav}<h1>{esc(x["h1"])}<small>{esc(x["sub"])}</small></h1><p class="lead">{esc(x["lead"])}</p>{secs}',
              [bld, org, {"@context": "https://schema.org", "@type": "WebPage", "name": x["h1"], "inLanguage": hl,
                          "url": site.site + f"{pre}terms/", "description": x["desc"], "publisher": {"@id": site.site}}])

        # ---- contact ----
        x = L["ct"]
        nav, bld = site.crumbs([(L["home"], pre), (x["crumb"], None)])
        items = "<dl>" + "".join(f'<div><dt>{esc(a)}</dt><dd>{b.replace("{policy}", policy)}</dd></div>' for a, b in x["items"]) + "</dl>"
        cant = '<ul class="x">' + "".join(f"<li>{esc(c)}</li>" for c in x["cant"]) + "</ul>"
        shell(lang, pre, hl, "ct", "contact",
              f'{nav}<h1>{esc(x["h1"])}<small>{esc(x["sub"])}</small></h1><p class="lead">{esc(x["lead"])}</p>'
              f'<a class="tgb" href="{TGURL}" target="_blank" rel="noopener">{TG}{esc(x["tg"])}</a>'
              f'<h2>{esc(x["what"])}</h2>{items}'
              f'<h2>{esc(x["nb"])}</h2>{cant}'
              f'<div class="who"><b>{esc(x["who"])}</b><p>{esc(x["whop"])}</p></div>',
              [bld, org, {"@context": "https://schema.org", "@type": "ContactPage", "name": x["h1"], "inLanguage": hl,
                          "url": site.site + f"{pre}contact/", "description": x["desc"],
                          "mainEntity": {"@type": "Organization", "name": "4D Malam Ini", "url": site.site,
                                         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                                                          "url": TGURL, "availableLanguage": ["en", "ms", "zh", "ta"]}}}])
