"""Info hub: /info/ (+ /ms/ /zh/ /ta/). Company profiles, draw days, short how-to-play, play responsibly.
The full guide stays at /guide/ and is linked from the How to play section."""
from html import escape as esc

LANGS = {"en": ("en", ""), "ms": ("ms", "ms/"), "zh": ("zh-Hans", "zh/"), "ta": ("ta", "ta/")}
# key, name, chinese, header colour, accent, logo file, founded/“since” value, official about page, chips
CO = [
    ("M", "Magnum 4D", "万能", "#FFF200", "#E9C46B", "m", "1968", "https://www.magnum.my/CorporateProfile.aspx", ["4D", "4D Jackpot", "4D Jackpot Gold", "Magnum Life"]),
    ("T", "Sports Toto", "多多", "#C00000", "#FF5A5F", "t-n", "1969", "https://www.sportstoto.com.my/corporate_aboutus.asp", ["4D", "4D Jackpot", "5D", "6D", "Star 6/50", "Power 6/55", "Supreme 6/58"]),
    ("D", "Da Ma Cai", "大马彩", "#000080", "#4C8DFF", "d-n", "1988", "https://www.damacai.com.my/about-us", ["1+3D", "Super 1+3D", "3D", "1+3D Jackpot", "3D Jackpot", "3+3D Bonus"]),
    ("G", "GD Lotto", "豪龙", "#B0121B", "#F27BA5", "g", None, "https://gdlotto.com/aboutus/", ["4D", "Live"]),
    ("N", "9 Lotto", "", "#0E8F86", "#2EC4B6", "n-w", None, "https://9lotto.com/result", ["4D", "7pm", "9pm"]),
]
PRIZES = [("RM2,500", "RM3,500"), ("RM1,000", "RM2,000"), ("RM500", "RM1,000"), ("RM180", "–"), ("RM60", "–")]

T = {
"en": dict(
 title="4D Info: Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto", desc="Who runs each Malaysian 4D draw, when they draw, how to play Big and Small, and how to play responsibly.",
 crumb="Info", home="Home", h1="Info", lead="Who runs each 4D draw, when they draw, and how to play: everything behind the results board in one place.",
 tabs=("Companies", "Draw days", "How to play", "Play responsibly"),
 s1="The companies", s1s="Five draws on one board. Here is who is behind each one.",
 since="Since", draws="Draws", daily="Daily", twice="2× daily", res="Latest results", off="Official site",
 sub={"M": "Magnum Corporation Sdn Bhd", "T": "STM Lottery Sdn Bhd", "D": "Pan Malaysian Pools Sdn Bhd", "G": "Grand Dragon Lotto", "N": "Two draws a day"},
 intro={"M": "Malaysia's original 4D company and the name most players grew up with. Magnum runs the licensed 4-Digit forecast game and its variations, and is owned by Magnum Berhad, which is listed on Bursa Malaysia.",
        "T": "Set up by the Malaysian Government in 1969 to raise funds for sports, youth and cultural activities, and privatised in 1985. Today it is Malaysia's only national lotto operator, running 4D, 5D, 6D and the big jackpot lotto games.",
        "D": "Runs the 1+3D game under the Racing (Totalisator Board) Act 1961. Since 2011 it has been a social business: its dividends go to The Community Chest, which builds and repairs facilities at Chinese, Tamil and mission schools across Malaysia.",
        "G": "Grand Dragon Lotto is a 4D draw based in Cambodia, known for broadcasting its results live. It draws every evening, so there is a result even on days the Malaysian companies are off.",
        "N": "A daily 4D draw with two results each evening, at 7pm and 9pm. The board shows both draws as separate slips, and on days without a Magnum, Toto or Da Ma Cai draw they appear first."},
 facts={"M": [("Group", "Magnum Berhad (Bursa-listed since 1982)"), ("Draws", "Wed, Sat, Sun · 7pm + special Tuesdays")],
        "T": [("Group", "Sports Toto Berhad (formerly Berjaya Sports Toto)"), ("Draws", "Wed, Sat, Sun · 7pm + special Tuesdays")],
        "D": [("Owner", "Jana Pendidikan Malaysia (since 2011)"), ("Draws", "Wed, Sat, Sun · 7pm + special Tuesdays")],
        "G": [("Based in", "Phnom Penh, Cambodia"), ("Draws", "Every day · 7pm")],
        "N": [("Draws", "Every day · 7pm and 9pm")]},
 s2="Draw days", s2s="All times are Malaysia time. Results appear on the board within minutes.",
 days=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), sp="sp", spn="sp = special draw. The companies announce these in advance, usually on a Tuesday.", n9="7pm & 9pm, every day",
 s3="How to play 4D", s3s="The short version. Tap a step to open it.",
 steps=[("Pick a 4-digit number", "<p>Any number from 0000 to 9999. Every number has the same chance in each draw. Many players use birthdays, car plates or a dream looked up in the 4D dictionary.</p>"),
        ("Big or Small", "<p>Each draw has 23 winning numbers. <b>Big</b> wins on all 23; <b>Small</b> only on the top 3 but pays more.</p>"),
        ("Box, iBox and Roll", "<p><b>Box</b> buys every order of your digits (1234 = 24 bets). <b>iBox</b> covers every order for one stake, with the prize divided. <b>Roll</b> turns one digit into 0–9.</p>"),
        ("Your real chances", "<p>About 1 in 435 for any Big prize, 1 in 3,333 for Small. Prizes pay back roughly 64–65 sen per RM1 over time.</p>"),
        ("Claiming a prize", "<p>Buy only from licensed outlets, keep your ticket safe and check the claim deadline on the company's official page.</p>")],
 pz=("Per RM1", "Big", "Small", ("1st", "2nd", "3rd", "Special ×10", "Consolation ×10")),
 more="Full guide, with company-by-company rules ›",
 s4="Play responsibly", r1="Only non-Muslims aged 21 and above may buy tickets or claim prizes in Malaysia.",
 r2="Set a budget, never chase losses, and take a break if it stops being fun. 4D is entertainment with a cost, never income.",
 src="4D Malam Ini is an independent results site, not affiliated with any operator. Company details are summarised from each operator's own pages and annual reports; their official pages always take priority."),
"ms": dict(
 title="Info 4D: Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto", desc="Siapa yang mengendalikan setiap cabutan 4D Malaysia, hari cabutan, cara main Big dan Small, dan bermain secara bertanggungjawab.",
 crumb="Info", home="Utama", h1="Info", lead="Siapa yang mengendalikan setiap cabutan 4D, bila cabutan dibuat, dan cara bermain: semua di sebalik papan keputusan, di satu tempat.",
 tabs=("Syarikat", "Hari cabutan", "Cara main", "Main berhemah"),
 s1="Syarikat-syarikat", s1s="Lima cabutan dalam satu papan. Ini siapa di sebalik setiap satu.",
 since="Sejak", draws="Cabutan", daily="Setiap hari", twice="2× sehari", res="Keputusan terkini", off="Laman rasmi",
 sub={"M": "Magnum Corporation Sdn Bhd", "T": "STM Lottery Sdn Bhd", "D": "Pan Malaysian Pools Sdn Bhd", "G": "Grand Dragon Lotto", "N": "Dua cabutan sehari"},
 intro={"M": "Syarikat 4D yang asal di Malaysia dan nama yang paling dikenali pemain. Magnum mengendalikan permainan ramalan 4-Digit berlesen serta variasinya, dan dimiliki oleh Magnum Berhad yang tersenarai di Bursa Malaysia.",
        "T": "Ditubuhkan oleh Kerajaan Malaysia pada 1969 untuk mengumpul dana bagi sukan, belia dan kebudayaan, dan diswastakan pada 1985. Kini satu-satunya pengendali loto nasional Malaysia, dengan 4D, 5D, 6D dan permainan loto jackpot besar.",
        "D": "Mengendalikan permainan 1+3D di bawah Akta Lumba Kuda (Lembaga Totalisator) 1961. Sejak 2011 ia sebuah perniagaan sosial: dividennya disalurkan kepada The Community Chest, yang membina dan membaiki kemudahan sekolah Cina, Tamil dan mubaligh di seluruh Malaysia.",
        "G": "Grand Dragon Lotto ialah cabutan 4D yang berpangkalan di Kemboja, terkenal dengan siaran keputusan secara langsung. Cabutan setiap petang, jadi ada keputusan walaupun syarikat Malaysia tiada cabutan.",
        "N": "Cabutan 4D harian dengan dua keputusan setiap petang, pada 7 malam dan 9 malam. Papan menunjukkan kedua-duanya sebagai slip berasingan, dan pada hari tanpa cabutan Magnum, Toto atau Da Ma Cai ia dipaparkan dahulu."},
 facts={"M": [("Kumpulan", "Magnum Berhad (tersenarai di Bursa sejak 1982)"), ("Cabutan", "Rabu, Sabtu, Ahad · 7 mlm + Selasa khas")],
        "T": [("Kumpulan", "Sports Toto Berhad (dahulu Berjaya Sports Toto)"), ("Cabutan", "Rabu, Sabtu, Ahad · 7 mlm + Selasa khas")],
        "D": [("Pemilik", "Jana Pendidikan Malaysia (sejak 2011)"), ("Cabutan", "Rabu, Sabtu, Ahad · 7 mlm + Selasa khas")],
        "G": [("Pangkalan", "Phnom Penh, Kemboja"), ("Cabutan", "Setiap hari · 7 mlm")],
        "N": [("Cabutan", "Setiap hari · 7 mlm dan 9 mlm")]},
 s2="Hari cabutan", s2s="Semua waktu ialah waktu Malaysia. Keputusan muncul di papan dalam beberapa minit.",
 days=("Isn", "Sel", "Rab", "Kha", "Jum", "Sab", "Ahd"), sp="kh", spn="kh = cabutan khas. Syarikat mengumumkannya lebih awal, biasanya pada hari Selasa.", n9="7 mlm & 9 mlm, setiap hari",
 s3="Cara main 4D", s3s="Versi ringkas. Ketik satu langkah untuk membukanya.",
 steps=[("Pilih nombor 4 digit", "<p>Apa-apa nombor dari 0000 hingga 9999. Setiap nombor ada peluang yang sama dalam setiap cabutan. Ramai pemain guna tarikh lahir, nombor plat kereta atau mimpi yang dicari dalam kamus 4D.</p>"),
        ("Big atau Small", "<p>Setiap cabutan ada 23 nombor menang. <b>Big</b> menang pada kesemua 23; <b>Small</b> hanya pada 3 teratas tetapi bayarannya lebih tinggi.</p>"),
        ("Box, iBox dan Roll", "<p><b>Box</b> membeli setiap susunan digit anda (1234 = 24 pertaruhan). <b>iBox</b> meliputi semua susunan dengan satu taruhan, hadiah dibahagi. <b>Roll</b> menukar satu digit kepada 0–9.</p>"),
        ("Peluang sebenar", "<p>Kira-kira 1 dalam 435 untuk sebarang hadiah Big, 1 dalam 3,333 untuk Small. Dalam jangka panjang hadiah membayar balik kira-kira 64–65 sen bagi setiap RM1.</p>"),
        ("Menuntut hadiah", "<p>Beli hanya di cawangan berlesen, simpan tiket dengan selamat dan semak tarikh akhir tuntutan di laman rasmi syarikat.</p>")],
 pz=("Setiap RM1", "Big", "Small", ("Pertama", "Kedua", "Ketiga", "Istimewa ×10", "Saguhati ×10")),
 more="Panduan penuh, dengan peraturan setiap syarikat ›",
 s4="Main secara berhemah", r1="Hanya bukan Islam berumur 21 tahun ke atas boleh membeli tiket atau menuntut hadiah di Malaysia.",
 r2="Tetapkan bajet, jangan kejar kerugian, dan berehat jika ia tidak lagi menyeronokkan. 4D ialah hiburan yang ada kosnya, bukan pendapatan.",
 src="4D Malam Ini ialah laman keputusan bebas, tidak bergabung dengan mana-mana syarikat. Butiran syarikat diringkaskan daripada laman dan laporan tahunan syarikat sendiri; laman rasmi mereka sentiasa diutamakan."),
"zh": dict(
 title="万字资讯：万能、多多、大马彩、豪龙与 9 Lotto", desc="马来西亚各家万字公司简介、开彩日、大字小字玩法，以及理性投注须知。",
 crumb="资讯", home="首页", h1="资讯", lead="每家万字公司是谁、几时开彩、怎么玩：成绩板背后的一切，都在这一页。",
 tabs=("公司简介", "开彩日", "玩法", "理性投注"),
 s1="万字公司", s1s="五家开彩，一个成绩板。以下是每一家的背景。",
 since="成立", draws="开彩", daily="每天", twice="每天2期", res="最新成绩", off="官方网站",
 sub={"M": "Magnum Corporation Sdn Bhd", "T": "STM Lottery Sdn Bhd", "D": "Pan Malaysian Pools Sdn Bhd", "G": "Grand Dragon Lotto", "N": "每天开彩两次"},
 intro={"M": "马来西亚最早的万字公司，也是许多人从小就熟悉的名字。万能经营持牌的四位数字预测游戏及其变化玩法，母公司万能有限公司在马来西亚交易所上市。",
        "T": "1969年由马来西亚政府成立，为体育、青年及文化活动筹募资金，1985年私营化。如今是马来西亚唯一的全国乐透经营商，经营4D、5D、6D及大型积宝乐透。",
        "D": "根据1961年赛马（赌金计算局）法令经营1+3D。自2011年起成为社会企业：股息拨给公益金（The Community Chest），用于兴建和维修全国华小、淡小及教会学校的设施。",
        "G": "豪龙（Grand Dragon Lotto）是总部设在柬埔寨的万字开彩，以现场直播开彩闻名。每天晚上开彩，所以大马公司休息的日子也有成绩。",
        "N": "每天开彩两次的万字，分别在晚上7点和9点。成绩板把两期分开显示；在万能、多多、大马彩没有开彩的日子，会排在最前面。"},
 facts={"M": [("集团", "万能有限公司（1982年起上市）"), ("开彩", "星期三、六、日 · 晚上7点 + 特别星期二")],
        "T": [("集团", "Sports Toto Berhad（前称成功多多）"), ("开彩", "星期三、六、日 · 晚上7点 + 特别星期二")],
        "D": [("拥有者", "Jana Pendidikan Malaysia（2011年起）"), ("开彩", "星期三、六、日 · 晚上7点 + 特别星期二")],
        "G": [("总部", "柬埔寨金边"), ("开彩", "每天 · 晚上7点")],
        "N": [("开彩", "每天 · 晚上7点及9点")]},
 s2="开彩日", s2s="全部为马来西亚时间。成绩会在几分钟内出现在成绩板上。",
 days=("一", "二", "三", "四", "五", "六", "日"), sp="特", spn="特 = 特别开彩，公司会提前宣布，通常在星期二。", n9="每天晚上7点和9点",
 s3="万字怎么玩", s3s="简单版本，点击步骤展开。",
 steps=[("选一个四位号码", "<p>0000 到 9999 任何号码，每期每个号码的机会都一样。很多人用生日、车牌，或在万字字典里查梦。</p>"),
        ("大字或小字", "<p>每期有23个中奖号码。<b>大字</b>23个都可中；<b>小字</b>只中头三奖，但奖金更高。</p>"),
        ("包字、iBox 和 Roll", "<p><b>包字</b>买下号码的所有排列（1234 = 24注）。<b>iBox</b>一注包所有排列，奖金按排列数平分。<b>Roll</b>把其中一位变成0–9。</p>"),
        ("真实中奖机会", "<p>大字中任何奖约 1/435，小字约 1/3,333。长期来看，每投注RM1约回报64–65仙。</p>"),
        ("领奖", "<p>只在持牌投注站购买，保管好彩票，并在公司官网查看领奖期限。</p>")],
 pz=("每RM1", "大字", "小字", ("头奖", "二奖", "三奖", "特别奖 ×10", "安慰奖 ×10")),
 more="完整攻略，含各公司规则 ›",
 s4="理性投注", r1="在马来西亚，只有21岁或以上的非穆斯林可以购买彩票或领奖。",
 r2="先定预算，不要追输，不好玩了就休息。万字是有成本的娱乐，不是收入。",
 src="4D Malam Ini 是独立的成绩网站，与任何公司无关。公司资料摘自各公司官网及年报；一切以官方网页为准。"),
"ta": dict(
 title="4D தகவல்: Magnum, Sports Toto, Da Ma Cai, GD Lotto & 9 Lotto", desc="மலேசிய 4D குலுக்கல்களை நடத்துபவர்கள், குலுக்கல் நாட்கள், Big மற்றும் Small விளையாடும் முறை, பொறுப்புடன் விளையாடுதல்.",
 crumb="தகவல்", home="முகப்பு", h1="தகவல்", lead="ஒவ்வொரு 4D குலுக்கலையும் யார் நடத்துகிறார்கள், எப்போது குலுக்கல், எப்படி விளையாடுவது: முடிவுப் பலகையின் பின்னால் உள்ள அனைத்தும் ஒரே இடத்தில்.",
 tabs=("நிறுவனங்கள்", "குலுக்கல் நாட்கள்", "விளையாடும் முறை", "பொறுப்புடன்"),
 s1="நிறுவனங்கள்", s1s="ஒரே பலகையில் ஐந்து குலுக்கல்கள். ஒவ்வொன்றின் பின்னணி இதோ.",
 since="முதல்", draws="குலுக்கல்", daily="தினமும்", twice="தினம் 2×", res="சமீபத்திய முடிவுகள்", off="அதிகாரப்பூர்வ தளம்",
 sub={"M": "Magnum Corporation Sdn Bhd", "T": "STM Lottery Sdn Bhd", "D": "Pan Malaysian Pools Sdn Bhd", "G": "Grand Dragon Lotto", "N": "தினமும் இரண்டு குலுக்கல்கள்"},
 intro={"M": "மலேசியாவின் முதல் 4D நிறுவனம்; பெரும்பாலான விளையாட்டாளர்களுக்குப் பழக்கமான பெயர். உரிமம் பெற்ற 4-இலக்க முன்கணிப்பு விளையாட்டையும் அதன் வகைகளையும் நடத்துகிறது; Bursa Malaysia-வில் பட்டியலிடப்பட்ட Magnum Berhad இதன் உரிமையாளர்.",
        "T": "விளையாட்டு, இளைஞர் மற்றும் கலாச்சார நடவடிக்கைகளுக்கு நிதி திரட்ட 1969-இல் மலேசிய அரசால் தொடங்கப்பட்டு, 1985-இல் தனியார்மயமாக்கப்பட்டது. இன்று மலேசியாவின் ஒரே தேசிய லோட்டோ நிறுவனம்; 4D, 5D, 6D மற்றும் பெரிய ஜாக்பாட் லோட்டோ விளையாட்டுகள்.",
        "D": "1961 குதிரைப் பந்தய (டோட்டலைசேட்டர் வாரியம்) சட்டத்தின் கீழ் 1+3D விளையாட்டை நடத்துகிறது. 2011 முதல் சமூக நிறுவனம்: அதன் ஈவுத்தொகை The Community Chest-க்குச் செல்கிறது; அது நாடு முழுவதும் சீன, தமிழ் மற்றும் மிஷன் பள்ளிகளின் வசதிகளைக் கட்டி, பழுது பார்க்கிறது.",
        "G": "Grand Dragon Lotto கம்போடியாவைத் தளமாகக் கொண்ட 4D குலுக்கல்; முடிவுகளை நேரலையாக ஒளிபரப்புவதற்குப் பெயர் பெற்றது. தினமும் மாலை குலுக்கல் இருப்பதால், மலேசிய நிறுவனங்கள் ஓய்வெடுக்கும் நாட்களிலும் முடிவு உண்டு.",
        "N": "தினமும் இரவு 7 மணிக்கும் 9 மணிக்கும் இரண்டு முடிவுகள் கொண்ட 4D குலுக்கல். பலகை இரண்டையும் தனித்தனி சீட்டுகளாகக் காட்டும்; Magnum, Toto, Da Ma Cai குலுக்கல் இல்லாத நாட்களில் அவை முதலில் வரும்."},
 facts={"M": [("குழுமம்", "Magnum Berhad (1982 முதல் Bursa-வில்)"), ("குலுக்கல்", "புதன், சனி, ஞாயிறு · இரவு 7 + சிறப்பு செவ்வாய்")],
        "T": [("குழுமம்", "Sports Toto Berhad (முன்பு Berjaya Sports Toto)"), ("குலுக்கல்", "புதன், சனி, ஞாயிறு · இரவு 7 + சிறப்பு செவ்வாய்")],
        "D": [("உரிமையாளர்", "Jana Pendidikan Malaysia (2011 முதல்)"), ("குலுக்கல்", "புதன், சனி, ஞாயிறு · இரவு 7 + சிறப்பு செவ்வாய்")],
        "G": [("தளம்", "புனோம் பென், கம்போடியா"), ("குலுக்கல்", "தினமும் · இரவு 7")],
        "N": [("குலுக்கல்", "தினமும் · இரவு 7 மற்றும் 9")]},
 s2="குலுக்கல் நாட்கள்", s2s="அனைத்தும் மலேசிய நேரம். முடிவுகள் சில நிமிடங்களில் பலகையில் தோன்றும்.",
 days=("தி", "செ", "பு", "வி", "வெ", "ச", "ஞா"), sp="சி", spn="சி = சிறப்பு குலுக்கல். நிறுவனங்கள் முன்கூட்டியே அறிவிக்கும், பொதுவாக செவ்வாய்க்கிழமை.", n9="தினமும் இரவு 7 & 9",
 s3="4D விளையாடுவது எப்படி", s3s="சுருக்கமான வடிவம். திறக்க ஒரு படியைத் தட்டவும்.",
 steps=[("4 இலக்க எண்ணைத் தேர்ந்தெடுங்கள்", "<p>0000 முதல் 9999 வரை எந்த எண்ணும். ஒவ்வொரு குலுக்கலிலும் எல்லா எண்களுக்கும் ஒரே வாய்ப்பு. பலர் பிறந்தநாள், கார் எண் அல்லது 4D அகராதியில் தேடிய கனவைப் பயன்படுத்துவர்.</p>"),
        ("Big அல்லது Small", "<p>ஒவ்வொரு குலுக்கலிலும் 23 வெற்றி எண்கள். <b>Big</b> 23-இலும் வெல்லும்; <b>Small</b> முதல் 3-இல் மட்டும், ஆனால் அதிகம் தரும்.</p>"),
        ("Box, iBox மற்றும் Roll", "<p><b>Box</b> உங்கள் இலக்கங்களின் எல்லா வரிசைகளையும் வாங்கும் (1234 = 24 பந்தயங்கள்). <b>iBox</b> ஒரே பந்தயத்தில் எல்லா வரிசைகளையும் உள்ளடக்கும், பரிசு பகிரப்படும். <b>Roll</b> ஒரு இலக்கத்தை 0–9 ஆக்கும்.</p>"),
        ("உண்மையான வாய்ப்புகள்", "<p>Big-இல் ஏதாவது பரிசுக்கு சுமார் 435-இல் 1, Small-இல் 3,333-இல் 1. நீண்ட காலத்தில் ஒவ்வொரு RM1-க்கும் சுமார் 64–65 சென் திரும்பும்.</p>"),
        ("பரிசைப் பெறுதல்", "<p>உரிமம் பெற்ற கடைகளில் மட்டும் வாங்குங்கள், சீட்டைப் பாதுகாப்பாக வைத்திருங்கள், நிறுவனத்தின் அதிகாரப்பூர்வ பக்கத்தில் கோரிக்கைக் காலக்கெடுவைச் சரிபாருங்கள்.</p>")],
 pz=("RM1-க்கு", "Big", "Small", ("முதல்", "இரண்டாம்", "மூன்றாம்", "சிறப்பு ×10", "ஆறுதல் ×10")),
 more="முழு வழிகாட்டி, நிறுவன வாரியான விதிகளுடன் ›",
 s4="பொறுப்புடன் விளையாடுங்கள்", r1="மலேசியாவில் 21 வயதுக்கு மேற்பட்ட முஸ்லிம் அல்லாதவர்கள் மட்டுமே சீட்டு வாங்கவோ பரிசு பெறவோ முடியும்.",
 r2="பட்ஜெட் வையுங்கள், இழப்பைத் துரத்தாதீர்கள், மகிழ்ச்சி இல்லையெனில் ஓய்வெடுங்கள். 4D செலவுள்ள பொழுதுபோக்கு, வருமானம் அல்ல.",
 src="4D Malam Ini ஒரு சுயாதீன முடிவுத் தளம்; எந்த நிறுவனத்துடனும் இணைந்ததல்ல. நிறுவன விவரங்கள் அவற்றின் சொந்தப் பக்கங்கள் மற்றும் ஆண்டறிக்கைகளிலிருந்து சுருக்கப்பட்டவை; அதிகாரப்பூர்வ பக்கங்களே இறுதி."),
}

CSS = """.info{--mu:#9DB0D3;--ln:rgba(255,255,255,.09);--cd:#0F1F3D;--gold:#E9C46B}
.info .itop{position:sticky;top:0;z-index:4;background:rgba(7,20,43,.93);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);margin:0 -16px;padding:8px 16px 0;border-bottom:1px solid var(--ln)}
.info .crumb{font-size:12.5px;color:var(--mu)}.info .crumb a{color:var(--mu)}
.info .lng{display:flex;gap:6px;float:right}.info .lng a{font-size:12px;font-weight:700;color:var(--mu);text-decoration:none;padding:2px 6px;border-radius:6px}.info .lng a[aria-current]{background:#13274A;color:#fff}
.info .tabs{clear:both;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;padding:10px 0}
.info .tabs a{display:flex;align-items:center;justify-content:center;text-align:center;min-height:36px;text-decoration:none;font-size:12.5px;line-height:1.2;font-weight:700;padding:5px 4px;border-radius:12px;background:#13274A;color:var(--mu);border:1px solid var(--ln);overflow-wrap:anywhere}
.info [lang=ta] .tabs a,.info .tabs a:lang(ta){font-size:11px}.info .tabs a.on{background:var(--gold);color:#1B1300;border-color:transparent}
.info .hero{padding:20px 0 4px}.info h1{margin:0;font-size:28px;letter-spacing:-.02em}.info .hero p{margin:6px 0 0;color:var(--mu);max-width:640px}
.info section{padding-top:26px;scroll-margin-top:110px}
.info h2{font-size:20px;margin:0 0 4px;display:flex;align-items:center;gap:10px}.info h2 i{font-style:normal;display:grid;place-items:center;width:28px;height:28px;border-radius:9px;background:rgba(233,196,107,.15);color:var(--gold);font-size:14px}
.info .sub{color:var(--mu);margin:0 0 14px;font-size:14px}
.info .co{display:grid;gap:14px}@media(min-width:760px){.info .co{grid-template-columns:repeat(2,minmax(0,1fr))}}
.info .cc{background:var(--cd);border:1px solid var(--ln);border-radius:18px;overflow:hidden;display:flex;flex-direction:column}
.info .ch{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--hb);color:#fff}.info .k-M .ch{color:#111}.info .k-G .ch{color:#FFE7A3}
.info .ch img{height:40px;width:48px;object-fit:contain;flex:none;filter:drop-shadow(0 1px 2px rgba(0,0,0,.25))}.info .k-N .ch img{width:110px;height:24px}
.info .ch b{display:block;font-size:17.5px;line-height:1.2}.info .ch b i{font-style:normal;opacity:.9}.info .ch small{display:block;font-size:12.5px;font-weight:700;opacity:.85}
.info .since{margin-left:auto;text-align:right;flex:none;font-weight:800;line-height:1.05}.info .since small{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase}.info .since span{font-size:21px}
.info .cb{padding:14px 16px 4px;flex:1}.info .cb p{margin:0 0 12px;color:#D3DDF2}
.info dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0 0 12px;font-size:13.5px}.info dt{color:var(--mu)}.info dd{margin:0;font-weight:600}
.info .chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}.info .chips span{font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px;background:rgba(255,255,255,.06);border:1px solid var(--ln)}
.info .cf{display:flex;gap:8px;padding:0 16px 16px}.info .cf a{flex:1;text-align:center;text-decoration:none;font-weight:700;font-size:13.5px;padding:9px 6px;border-radius:12px;border:1px solid var(--ln);background:#13274A;color:#EAF0FF}.info .cf a.p{background:var(--c);color:#0A1428;border-color:transparent}
.info .sch{background:var(--cd);border:1px solid var(--ln);border-radius:18px;overflow-x:auto}
.info .sch table{width:100%;border-collapse:collapse;font-size:13px;text-align:center}.info .sch th,.info .sch td{padding:9px 3px;border-bottom:1px solid var(--ln);white-space:nowrap}.info .sch th{color:var(--mu);font-size:12px}
.info .sch td:first-child{text-align:left;padding-left:12px;font-weight:700}.info .sch tr:last-child td{border-bottom:0}.info .dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c);margin-right:4px}.info .sch em{font-style:normal;color:var(--mu)}
.info .note{font-size:12.5px;color:var(--mu);margin:8px 2px 0}
.info .acc{display:grid;gap:8px}.info details{background:var(--cd);border:1px solid var(--ln);border-radius:14px}
.info summary{list-style:none;cursor:pointer;padding:13px 16px;font-weight:700;display:flex;align-items:center;gap:10px}.info summary::-webkit-details-marker{display:none}
.info summary i{font-style:normal;width:24px;height:24px;border-radius:8px;display:grid;place-items:center;background:rgba(255,255,255,.07);font-size:12.5px;flex:none}
.info summary::after{content:"+";margin-left:auto;color:var(--gold);font-size:20px;line-height:1}.info details[open] summary::after{content:"–"}
.info details .bd{padding:0 16px 14px;color:#D3DDF2;font-size:14px}.info details .bd p{margin:0 0 8px}
.info .pz{width:100%;border-collapse:collapse;font-size:13px;margin:4px 0 8px}.info .pz th,.info .pz td{padding:6px 4px;border-bottom:1px solid var(--ln);text-align:right}.info .pz th:first-child,.info .pz td:first-child{text-align:left}.info .pz th{color:var(--mu)}
.info .more{display:inline-block;margin-top:10px;font-weight:700;color:var(--gold);text-decoration:none}
.info .rp{display:flex;gap:14px;align-items:flex-start;background:linear-gradient(135deg,rgba(255,90,95,.12),rgba(233,196,107,.08));border:1px solid rgba(255,90,95,.3);border-radius:18px;padding:16px}
.info .rp b.a{flex:none;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;font-size:18px;background:#FF5A5F;color:#fff}.info .rp p{margin:0 0 6px;font-size:14px;color:#D3DDF2}
.info .src{font-size:12px;color:var(--mu);margin:22px 0 0;border-top:1px solid var(--ln);padding-top:12px}"""

JS = ("<script>(function(){var t=[].slice.call(document.querySelectorAll('.info .tabs a'));if(!('IntersectionObserver'in window))return;"
      "var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)t.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})})},{rootMargin:'-120px 0px -60% 0px'});"
      "t.forEach(function(a){var s=document.querySelector(a.getAttribute('href'));if(s)io.observe(s)})})()</script>")

SCHED = {"M": "s", "T": "s", "D": "s"}  # Wed/Sat/Sun + special Tue


def build(site) -> None:
    import hashlib
    css_name = "assets/i." + hashlib.sha256(CSS.encode()).hexdigest()[:8] + ".css"
    (site.out / "assets").mkdir(exist_ok=True)
    (site.out / css_name).write_text(CSS)
    cssl = f'<link rel="stylesheet" href="{site.u(css_name)}">'
    path = lambda l: LANGS[l][1] + "info/"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l][0]}" href="{site.site}{path(l)}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{site.site}info/">'
    names = {"en": "EN", "ms": "BM", "zh": "中文", "ta": "தமிழ்"}
    for lang, x in T.items():
        hl, pre = LANGS[lang]
        home = site.u(pre)
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        ids = ("companies", "schedule", "guide", "responsible")
        top = (f'<div class="itop">{lng}<div class="crumb"><a href="{home}">{esc(x["home"])}</a> › <b>{esc(x["crumb"])}</b></div>'
               '<nav class="tabs" aria-label="Sections">' + "".join(f'<a href="#{i}"' + (' class="on"' if n == 0 else "") + f'>{esc(t_)}</a>' for n, (i, t_) in enumerate(zip(ids, x["tabs"]))) + "</nav></div>")
        cards = ""
        for k, name, zh, hb, c, logo, since, url, chips in CO:
            sv = f'<small>{esc(x["since"])}</small><br><span>{since}</span>' if since else f'<small>{esc(x["draws"])}</small><br><span>{esc(x["twice"] if k == "N" else x["daily"])}</span>'
            zhh = f' <i>{zh}</i>' if zh and lang != "zh" else ""
            nm = (zh if lang == "zh" and zh else name)
            alt = ' alt="9 Lotto"' if k == "N" else ' alt=""'
            wh = 'width="110" height="24"' if k == "N" else 'width="48" height="40"'
            cards += (f'<article class="cc k-{k}" style="--hb:{hb};--c:{c}"><div class="ch"><img src="{site.u("img/op/" + logo + ".webp?v=3")}" {wh}{alt} loading="lazy">'
                      f'<div><b>{esc(nm)}{zhh}</b><small>{esc(x["sub"][k])}</small></div><div class="since">{sv}</div></div>'
                      f'<div class="cb"><p>{esc(x["intro"][k])}</p><dl>' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in x["facts"][k]) + "</dl>"
                      '<div class="chips">' + "".join(f"<span>{esc(ch)}</span>" for ch in chips) + "</div></div>"
                      f'<div class="cf"><a class="p" href="{home}#rc-{k}">{esc(x["res"])}</a><a href="{url}" target="_blank" rel="noopener nofollow">{esc(x["off"])} ›</a></div></article>')
        rows = ""
        for k, name, zh, hb, c, *_ in CO:
            nm = (zh if lang == "zh" and zh else name.replace(" 4D", ""))
            if k == "N":
                cells = f'<td colspan="7">{esc(x["n9"])}</td>'
            elif k == "G":
                cells = "<td>7pm</td>" * 7
            else:
                cells = f'<td>–</td><td><em>{esc(x["sp"])}</em></td><td>7pm</td><td>–</td><td>–</td><td>7pm</td><td>7pm</td>'
            rows += f'<tr><td><span class="dot" style="--c:{c}"></span>{esc(nm)}</td>{cells}</tr>'
        sched = '<div class="sch"><table><tr><th></th>' + "".join(f"<th>{esc(d)}</th>" for d in x["days"]) + f"</tr>{rows}</table></div>"
        p0, p1, p2, rl = x["pz"]
        pz = f'<table class="pz"><tr><th>{esc(p0)}</th><th>{esc(p1)}</th><th>{esc(p2)}</th></tr>' + "".join(f"<tr><td>{esc(r)}</td><td>{b}</td><td>{s}</td></tr>" for r, (b, s) in zip(rl, PRIZES)) + "</table>"
        acc = '<div class="acc">' + "".join(
            f'<details{" open" if n == 0 else ""}><summary><i>{n + 1}</i>{esc(t_)}</summary><div class="bd">{h}{pz if n == 1 else ""}</div></details>' for n, (t_, h) in enumerate(x["steps"])) + "</div>"
        body = (f'<div class="info">{top}<div class="hero"><h1>{esc(x["h1"])}</h1><p>{esc(x["lead"])}</p></div>'
                f'<section id="companies"><h2><i>1</i>{esc(x["s1"])}</h2><p class="sub">{esc(x["s1s"])}</p><div class="co">{cards}</div></section>'
                f'<section id="schedule"><h2><i>2</i>{esc(x["s2"])}</h2><p class="sub">{esc(x["s2s"])}</p>{sched}<p class="note">{esc(x["spn"])}</p></section>'
                f'<section id="guide"><h2><i>3</i>{esc(x["s3"])}</h2><p class="sub">{esc(x["s3s"])}</p>{acc}<a class="more" href="{site.u(pre + "guide/")}">{esc(x["more"])}</a></section>'
                f'<section id="responsible"><h2><i>4</i>{esc(x["s4"])}</h2><div class="rp"><b class="a">21+</b><div><p>{esc(x["r1"])}</p><p>{esc(x["r2"])}</p></div></div>'
                f'<p class="src">{esc(x["src"])}</p></section></div>{JS}')
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        orgs = {"@context": "https://schema.org", "@type": "WebPage", "name": x["title"], "inLanguage": hl, "description": x["desc"],
                "about": [{"@type": "Organization", "name": n, "url": u} for _, n, _, _, _, _, _, u, _ in CO]}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"], body, lang=hl, ld=[bld, orgs], head=cssl + alts)
