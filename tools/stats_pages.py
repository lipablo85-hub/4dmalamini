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
            flab='Filter by company', allco='ALL', scope='Showing <b>{who}</b> · {n} draws · {w} winning numbers · {u} different numbers seen', mkt='Magnum, Da Ma Cai and Sports Toto', alln='all ten companies', jk='Super J3 and Super J9', thin='Not enough draws from this company yet.', 
            desc="Malaysia 4D statistics from {n} draws since {s}: most drawn numbers, numbers missing longest, top-3 regulars and digit frequency by position.",
            h1="4D statistics", lead="What {n} draws across 10 companies since {s} say about every 4D number. Updated after every draw.",
            k=("Draws analysed", "Numbers drawn"),
            hot="Most drawn numbers", hots="Every prize tier, since {s}.", cold="Missing longest", colds="Numbers that won before but have not appeared for the longest time.",
            rec="Hot in the last 90 days", recs="Most wins since {d}.", top="Top-3 prize regulars", tops="Most times in 1st, 2nd or 3rd prize.",
            dig="Digit frequency by position", digs="How often each digit appears in each of the 4 positions, as a share of that position.", dlo="less often", dhi="more often", pos=("1st digit", "2nd digit", "3rd digit", "4th digit"),
            box="Most frequent Box families", boxs="All arrangements of the same 4 digits counted together.", combos="{n} arrangements",
            times="×", alltime="all-time {n}×", days="{n}d", last="last", never="{n} numbers have never been drawn since {s}.",
            note="These are past results only. Every draw is independent, so past frequency does not make any number more or less likely to win. 21+ · Non-Muslims only · Play responsibly.",
            more="Check any number", pop="Popular 4D numbers"),
 "ms": dict(title="Statistik 4D: Nombor Panas & Sejuk, Kekerapan Digit", crumb="Statistik 4D", home="Utama",
            flab='Tapis ikut syarikat', allco='SEMUA', scope='Menunjukkan <b>{who}</b> · {n} cabutan · {w} nombor menang · {u} nombor berbeza', mkt='Magnum, Da Ma Cai dan Sports Toto', alln='kesemua sepuluh syarikat', jk='Super J3 dan Super J9', thin='Belum cukup cabutan daripada syarikat ini.', 
            desc="Statistik 4D Malaysia daripada {n} cabutan sejak {s}: nombor paling kerap, nombor paling lama tidak keluar, hadiah 1–3, kekerapan digit dan keluarga Box.",
            h1="Statistik 4D", lead="Apa yang {n} cabutan dari 10 syarikat sejak {s} tunjukkan tentang setiap nombor 4D. Dikemas kini selepas setiap cabutan.",
            k=("Cabutan dianalisis", "Nombor dicabut"),
            hot="Nombor paling kerap", hots="Semua peringkat hadiah, sejak {s}.", cold="Paling lama tidak keluar", colds="Nombor yang pernah menang tetapi paling lama tidak muncul.",
            rec="Panas dalam 90 hari", recs="Paling banyak menang sejak {d}.", top="Kerap dalam hadiah 1–3", tops="Paling kerap dalam hadiah Pertama, Kedua atau Ketiga.",
            dig="Kekerapan digit mengikut kedudukan", digs="Berapa kerap setiap digit muncul di setiap kedudukan, sebagai peratusan.", dlo="kurang kerap", dhi="lebih kerap", pos=("Digit 1", "Digit 2", "Digit 3", "Digit 4"),
            box="Keluarga Box paling kerap", boxs="Semua susunan 4 digit yang sama dikira bersama.", combos="{n} susunan",
            times="×", alltime="jumlah {n}×", days="{n}h", last="terakhir", never="{n} nombor belum pernah keluar sejak {s}.",
            note="Ini hanya keputusan lepas. Setiap cabutan adalah bebas, jadi kekerapan lepas tidak menjadikan mana-mana nombor lebih atau kurang berpeluang. 21+ · Bukan Islam sahaja · Main secara bertanggungjawab.",
            more="Semak mana-mana nombor", pop="Nombor 4D popular"),
 "zh": dict(title="万字统计：热门与冷门号码、数字出现频率", crumb="万字统计", home="首页",
            flab='按公司筛选', allco='全部', scope='显示 <b>{who}</b> · {n} 期 · {w} 个中奖号码 · {u} 个不同号码', mkt='万能、大马彩与多多', alln='全部十家公司', jk='Super J3 与 Super J9', thin='这家公司的开彩期数还不足。', 
            desc="根据{s}以来{n}期马来西亚万字开彩统计：最常开出号码、最久未开号码、前三奖常客、各位数字频率与 Box 号码组。",
            h1="万字统计", lead="{s}以来10家公司共{n}期开彩，每个万字号码的出现记录。每期开彩后更新。",
            k=("统计期数", "开出号码"),
            hot="最常开出的号码", hots="所有奖项，{s}至今。", cold="最久未开的号码", colds="曾经中过、但已经最久没有再出现的号码。",
            rec="近90天热门", recs="{d}以来中奖最多。", top="前三奖常客", tops="最常进入头奖、二奖或三奖。",
            dig="各位数字出现频率", digs="每个数字在4个位置出现的比例（%）。", dlo="较少", dhi="较多", pos=("第1位", "第2位", "第3位", "第4位"),
            box="最常开出的 Box 号码组", boxs="同样4个数字的所有排列合并计算。", combos="{n} 种排列",
            times="次", alltime="累计 {n} 次", days="{n} 天", last="最近", never="{s}以来有 {n} 个号码从未开出。",
            note="以上只是过往成绩。每期开彩都是独立的，过去出现次数不会让任何号码更容易或更难中奖。仅限21岁或以上非穆斯林 · 理性投注。",
            more="查询任何号码", pop="热门万字号码"),
 "ta": dict(title="4D புள்ளிவிவரம்: அதிகம் & குறைவாக வந்த எண்கள்", crumb="4D புள்ளிவிவரம்", home="முகப்பு",
            flab='நிறுவனம் வாரியாக வடிகட்டு', allco='அனைத்தும்', scope='காட்டுவது <b>{who}</b> · {n} குலுக்கல் · {w} வெற்றி எண்கள் · {u} வெவ்வேறு எண்கள்', mkt='Magnum, Da Ma Cai மற்றும் Sports Toto', alln='அனைத்து பத்து நிறுவனங்கள்', jk='Super J3 மற்றும் Super J9', thin='இந்த நிறுவனத்திடம் போதுமான குலுக்கல்கள் இல்லை.', 
            desc="{s} முதல் {n} குலுக்கல்களின் மலேசியா 4D புள்ளிவிவரம்: அதிகம் வந்த எண்கள், நீண்ட நாள் வராத எண்கள், முதல் 3 பரிசுகள், இலக்க அதிர்வெண், Box குடும்பங்கள்.",
            h1="4D புள்ளிவிவரம்", lead="{s} முதல் 10 நிறுவனங்களின் {n} குலுக்கல்கள் ஒவ்வொரு 4D எண்ணைப் பற்றியும் சொல்வது. ஒவ்வொரு குலுக்கலுக்குப் பின் புதுப்பிக்கப்படும்.",
            k=("ஆய்வு செய்த குலுக்கல்கள்", "வந்த எண்கள்"),
            hot="அதிகம் வந்த எண்கள்", hots="எல்லா பரிசுகளும், எல்லா நிறுவனங்களும், {s} முதல்.", cold="நீண்ட நாள் வராதவை", colds="முன்பு வென்று, நீண்ட காலமாக மீண்டும் வராத எண்கள்.",
            rec="கடந்த 90 நாளில் அதிகம்", recs="{d} முதல் அதிக வெற்றிகள்.", top="முதல் 3 பரிசில் அடிக்கடி", tops="1வது, 2வது, 3வது பரிசில் அதிக முறை.",
            dig="நிலை வாரியான இலக்க அதிர்வெண்", digs="4 நிலைகளிலும் ஒவ்வொரு இலக்கமும் வரும் விகிதம் (%).", dlo="குறைவு", dhi="அதிகம்", pos=("1வது இலக்கம்", "2வது இலக்கம்", "3வது இலக்கம்", "4வது இலக்கம்"),
            box="அதிகம் வந்த Box குடும்பங்கள்", boxs="அதே 4 இலக்கங்களின் எல்லா வரிசைகளும் சேர்த்து எண்ணப்படுகின்றன.", combos="{n} வரிசைகள்",
            times="×", alltime="மொத்தம் {n}×", days="{n}நா", last="கடைசி", never="{s} முதல் {n} எண்கள் ஒருமுறையும் வரவில்லை.",
            note="இவை கடந்த முடிவுகள் மட்டுமே. ஒவ்வொரு குலுக்கலும் தனித்தது; கடந்த அதிர்வெண் எந்த எண்ணின் வாய்ப்பையும் மாற்றாது. 21+ · முஸ்லிம் அல்லாதவர்கள் மட்டும் · பொறுப்புடன் விளையாடுங்கள்.",
            more="எந்த எண்ணையும் சரிபாருங்கள்", pop="பிரபல 4D எண்கள்"),
}

CSS = """.fw{position:sticky;top:0;z-index:6;margin:14px -14px 2px;padding:9px 0 8px;background:linear-gradient(var(--bg,#07142B) 74%,transparent)}
.flab{font-size:10.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#7E8DAB;padding:0 14px 8px}
.fstrip{position:relative}
.fstrip ul{display:flex;gap:8px;overflow-x:auto;padding:3px 14px 7px;margin:0;list-style:none;scroll-snap-type:x proximity;scrollbar-width:none}
.fstrip ul::-webkit-scrollbar{display:none}
.fstrip ul>li{flex:none;display:flex}
.fstrip::after{content:"";position:absolute;right:0;top:0;width:26px;height:100%;pointer-events:none;background:linear-gradient(90deg,transparent,var(--bg,#07142B))}
.fchip{flex:none;scroll-snap-align:start;position:relative;display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;
 border-radius:13px;border:1.5px solid #27406E;background:#0F1F3D;cursor:pointer;padding:0;transition:border-color .15s,background .15s,transform .12s}
.fchip i{width:28px;height:28px;border-radius:8px;background:url(/img/op/tk.webp) 0 0/280px 28px no-repeat;flex:none;display:block}
.fchip:active{transform:scale(.94)}
.fchip.on{border-color:#E9C46B;background:#1A2B4D;box-shadow:0 0 0 3px rgba(233,196,107,.17)}
.fchip.on::after{content:"";position:absolute;right:-3px;top:-3px;width:9px;height:9px;border-radius:50%;background:#E9C46B;border:2px solid var(--bg,#07142B)}
.fchip.w{width:auto;min-width:46px;padding:0 15px;font-weight:800;font-size:12.5px;line-height:1;letter-spacing:.05em;color:#C9D4EA;white-space:nowrap}
.fchip.w.on{color:#E9C46B}
.fchip.multi{gap:3px;padding:0 10px}
.fchip.multi i{width:21px;height:21px;border-radius:6px;background-size:210px 21px}
.scope{margin:0 0 4px;padding:9px 12px;border-radius:12px;background:#0C1A33;border:1px solid #1D3157;font-size:12.5px;line-height:1.45;color:#9FB0D3}
.scope b{color:#E9C46B}
.thin{font-size:12.5px;color:#8FA0C0;padding:10px 2px;margin:0}
.st4{--mu:#9DB0D3;--cd:#0F1F3D;--ln:#1D3157;--gold:#E9C46B;--ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei","Noto Sans Tamil",sans-serif;font-family:var(--ui)}
.st4 h1{font-size:26px;line-height:1.2;letter-spacing:-.4px;margin:6px 0 6px}
.st4 .lead{color:var(--mu);margin:0 0 16px;font-size:14px;line-height:1.55;max-width:34em}
.st4 .lng{display:flex;gap:6px;margin:4px 0 12px}
.st4 .lng a{padding:6px 11px;border-radius:999px;border:1px solid var(--ln);text-decoration:none;font-size:12.5px;font-weight:700;color:#C9D4EA}
.st4 .lng a[aria-current]{background:#F8F4E8;color:#07142B;border-color:#F8F4E8}
.st4 .kp{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
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
.st4 .hm em{font-style:normal;display:flex;align-items:center;color:#C9D4EA;font-weight:600;font-size:11px}.st4 .hleg{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:11px;color:var(--mu)}.st4 .hleg i{flex:1;height:8px;border-radius:4px;background:linear-gradient(90deg,#DC3C3C,#E9C46B,#4ADE80)}
.st4 .bx{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.st4 .bx a{padding:11px 13px;border-radius:14px;background:var(--cd);border:1px solid #233862;text-decoration:none}
.st4 .bx b{display:block;font:700 18px/1.1 var(--ui);font-variant-numeric:tabular-nums;color:#FFE7A3;letter-spacing:.06em}
.st4 .bx small{display:block;font-size:12px;color:var(--mu);margin-top:4px;line-height:1.3}.st4 .bx strong{color:#F8F4E8;font-weight:700}
.st4 .nt{margin-top:24px;padding:14px 16px;border-radius:14px;background:rgba(255,90,95,.08);border:1px solid rgba(255,90,95,.3);font-size:13px;color:#C2CEE4;line-height:1.6}
.st4 .cta2{display:flex;justify-content:center;align-items:center;height:48px;margin-top:8px;border-radius:999px;border:1px solid rgba(233,196,107,.4);color:var(--gold);font-weight:700;text-decoration:none;font-size:14px}
.st4 .cta{display:flex;justify-content:center;align-items:center;height:50px;margin-top:16px;border-radius:999px;background:var(--gold);color:#1A1405;font-weight:700;font-size:15px;text-decoration:none}

"""

JS = """(function(){
var P=__P__,D=P.d,M=P.m,L=P.l,cur="mkt";
var E=function(t){return String(t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})};
var nf=function(n){return n.toLocaleString("en-US")};
var fs=function(s){var y=s.slice(0,4),m=+s.slice(4,6);return L.zh?(m+"/"+y.slice(2)):(L.mon[m-1]+" "+y.slice(2))};
var link=function(n){return L.u4+n+"/"};
function rows(list,val,sub){
  if(!list.length)return '<p class="thin">'+E(L.thin)+"</p>";
  var mx=Math.max.apply(null,list.map(function(e){return e[1]}))||1;
  return "<ol>"+list.map(function(e,i){
    return '<li><a href="'+link(e[0])+'"><span class="r">'+(i+1)+'</span><span class="n">'+e[0]+'</span>'
      +'<span class="c">'+val(e)+'</span><span class="m">'+(M[e[0]]?E(M[e[0]]):"&nbsp;")+'</span>'
      +'<span class="d">'+sub(e)+'</span><u style="width:'+Math.max(6,Math.round(e[1]/mx*100))+'%"></u></a></li>';
  }).join("")+"</ol>";
}
function heat(pos){
  var flat=[],i,j;for(i=0;i<4;i++)for(j=0;j<10;j++)flat.push(pos[i][j]);
  var mn=Math.min.apply(null,flat),mx=Math.max.apply(null,flat);
  var col=function(v){var f=(v-mn)/Math.max(1,mx-mn),a=f<.5?[220,60,60]:[233,196,107],b=f<.5?[233,196,107]:[74,222,128],k=f<.5?f*2:(f-.5)*2;
    return "#"+a.map(function(c,q){return Math.round(c+(b[q]-c)*k).toString(16).padStart(2,"0")}).join("")};
  var h='<b></b>';for(j=0;j<10;j++)h+="<b>"+j+"</b>";
  var lab=document.querySelectorAll("#digits .hm em");
  for(i=0;i<4;i++){var t=pos[i].reduce(function(a,b){return a+b},0);
    h+="<em>"+(lab[i]?lab[i].textContent:"")+"</em>";
    for(j=0;j<10;j++)h+='<span title="'+nf(pos[i][j])+'" style="background:'+col(pos[i][j])+'">'+(pos[i][j]/t*100).toFixed(1)+"</span>";}
  return h;
}
function paint(){
  var d=D[cur];
  var sc=document.getElementById("scope");
  if(sc)sc.innerHTML=L.scope.replace("{who}",'<b>'+E(L.who[cur])+'</b>').replace("{n}",nf(d.nd)).replace("{w}",nf(d.t)).replace("{u}",nf(d.u));
  var kp=document.querySelectorAll(".kp b");if(kp[0])kp[0].textContent=nf(d.nd);if(kp[1])kp[1].textContent=nf(d.t);
  var set=function(id,html){var e=document.querySelector("#"+id+" .card");if(e)e.innerHTML=html};
  set("hot",rows(d.hot,function(e){return e[1]+L.times},function(e){return fs(e[2])}));
  set("cold",rows(d.cold,function(e){return E(L.days.replace("{n}",nf(e[1])))},function(e){return fs(e[2])}));
  set("recent",rows(d.rec,function(e){return e[1]+L.times},function(e){return E(L.alltime.replace("{n}",e[2]))}));
  set("top3",rows(d.top,function(e){return e[1]+L.times},function(e){return fs(e[2])}));
  var hm=document.querySelector("#digits .hm");if(hm)hm.innerHTML=heat(d.pos);
  var bx=document.querySelector("#box .bx");
  if(bx)bx.innerHTML=d.box.map(function(b){return '<a href="'+link(b[0])+'"><b>'+b[0]+'</b><small><strong>'+b[1]+(L.zh?"\\u6b21":"\\u00d7")
    +'</strong> \\u00b7 '+E(L.combos.replace("{n}",b[2]))+"</small></a>"}).join("");
}
document.querySelectorAll(".fchip").forEach(function(b){b.addEventListener("click",function(){
  if(b.dataset.f===cur)return;
  cur=b.dataset.f;
  document.querySelectorAll(".fchip").forEach(function(o){var on=o===b;o.classList.toggle("on",on);o.setAttribute("aria-pressed",on)});
  paint();
  b.scrollIntoView({inline:"center",block:"nearest",behavior:"smooth"});
})});
})();"""

def build(site) -> None:
    hits = site.hits
    dates = site.dates
    s0, s1 = dates[0], dates[-1]
    d8 = lambda d: dt.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    last = d8(s1)
    nd = site.ndraws
    NDALL = site.ndraws        # every draw, for copy that describes the dataset as a whole
    # Eleven filter states, each precomputed here rather than in the browser: shipping the raw
    # draw history would be ~400 KB, these are ~9 KB gzipped and switch instantly.
    FILT = [("mkt", "MDT"), ("all", "MDTGNSCHJK"), ("M", "M"), ("D", "D"), ("T", "T"), ("G", "G"),
            ("N", "N"), ("S", "S"), ("C", "C"), ("H", "H"), ("JK", "JK")]
    since90 = (last - dt.timedelta(days=90)).strftime("%Y%m%d")

    def agg(opsel):
        o = set(opsel)
        c = {}; lwin = {}; r90 = Counter(); t3 = Counter(); fm = defaultdict(int)
        ps = [[0] * 10 for _ in range(4)]; ndr = 0
        for n, v in hits.items():
            f = [h for h in v if h[1] in o]
            if not f:
                continue
            c[n] = len(f); lwin[n] = max(h[0] for h in f)
            r90[n] = sum(1 for h in f if h[0] >= since90)
            t3[n] = sum(1 for h in f if h[3] <= 3)
            fm["".join(sorted(n))] += len(f)
        for k, rws in site.draws.items():
            if k not in o:
                continue
            ndr += len(rws)
            for _, _, nums in rws:
                for val in nums:
                    for i, ch in enumerate(val):
                        ps[i][int(ch)] += 1
        return dict(cnt=c, lastwin=lwin, rc=r90, tc=t3, fam=fm, pos=ps, nd=ndr,
                    total=sum(c.values()), uniq=len(c),
                    hot=sorted(c, key=lambda n: (-c[n], -int(lwin[n])))[:12],
                    cold=sorted(c, key=lambda n: (lwin[n], n))[:12],
                    rec=[n for n, q in r90.most_common(12) if q],
                    top=[n for n, q in t3.most_common(12) if q],
                    boxes=sorted(fm, key=lambda k: -fm[k])[:12])

    ST = {fid: agg(ops) for fid, ops in FILT}
    DEF = "mkt"                      # what the page opens on, server-rendered for crawlers
    A = ST[DEF]
    cnt, lastwin, rc, tc, fam = A["cnt"], A["lastwin"], A["rc"], A["tc"], A["fam"]
    pos, hot, cold, rec, top, boxes = A["pos"], A["hot"], A["cold"], A["rec"], A["top"], A["boxes"]
    nd, total = A["nd"], A["total"]
    from itertools import permutations
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

        def hcol(v):
            # red (low) -> yellow (mid) -> green (high), on the share of that position's draws
            f = (v - mnp) / max(1, mxp - mnp)
            a_, b_ = ((220, 60, 60), (233, 196, 107)) if f < .5 else ((233, 196, 107), (74, 222, 128))
            k = f * 2 if f < .5 else (f - .5) * 2
            return "#%02X%02X%02X" % tuple(round(a_[i] + (b_[i] - a_[i]) * k) for i in range(3))
        hm = '<div class="hm"><b></b>' + "".join(f"<b>{d}</b>" for d in range(10))
        for i in range(4):
            hm += f'<em>{esc(x["pos"][i])}</em>' + "".join(
                f'<span title="{pos[i][d]:,}" style="background:{hcol(pos[i][d])}">{pos[i][d] / sum(pos[i]) * 100:.1f}</span>' for d in range(10))
        hm += f'</div><div class="hleg"><span>{esc(x["dlo"])}</span><i></i><span>{esc(x["dhi"])}</span></div>'
        bx = '<div class="bx">' + "".join(
            f'<a href="{site.u("4d/" + k + "/")}"><b>{k}</b><small><strong>{fam[k]}{"次" if lang == "zh" else "×"}</strong> · {esc(x["combos"].format(n=len(set(permutations(k)))))}</small></a>' for k in boxes) + "</div>"
        lng = '<nav class="lng" aria-label="Language">' + "".join(f'<a href="{site.u(path(l))}" hreflang="{LANGS[l][0]}"' + (' aria-current="page"' if l == lang else "") + f'>{names[l]}</a>' for l in LANGS) + "</nav>"
        kp = '<div class="kp">' + "".join(f"<div><b>{v}</b><small>{esc(lb)}</small></div>" for v, lb in zip((f"{nd:,}", f"{total:,}"), x["k"])) + "</div>"
        ids = [("hot", "🔥", x["hot"]), ("cold", "❄️", x["cold"]), ("recent", "📈", x["rec"]), ("top3", "🏆", x["top"]), ("digits", "🔢", x["dig"]), ("box", "🎲", x["box"])]
        tabs = '<nav class="tabs">' + "".join(f'<a href="#{i}">{ic} {esc(t)}</a>' for i, ic, t in ids) + "</nav>"
        sec = lambda i, ic, t, sub, body: f'<section id="{i}"><h2><i>{ic}</i>{esc(t)}</h2><p class="sub">{esc(sub)}</p>{body}</section>'
        def fscript():
            shown = set()
            for st in ST.values():
                shown |= set(st["hot"]) | set(st["cold"]) | set(st["rec"]) | set(st["top"])
            SD = {fid: {
                "nd": st["nd"], "t": st["total"], "u": st["uniq"],
                "hot": [[n, st["cnt"][n], st["lastwin"][n]] for n in st["hot"]],
                "cold": [[n, (last - d8(st["lastwin"][n])).days, st["lastwin"][n]] for n in st["cold"]],
                "rec": [[n, st["rc"][n], st["cnt"][n]] for n in st["rec"]],
                "top": [[n, st["tc"][n], st["lastwin"][n]] for n in st["top"]],
                "pos": st["pos"],
                "box": [[k, st["fam"][k], len(set(permutations(k)))] for k in st["boxes"]],
            } for fid, st in ST.items()}
            L = {"who": {k: WHO[k] for k in WHO}, "scope": x["scope"], "times": tm, "days": x["days"],
                 "alltime": x["alltime"], "combos": x["combos"], "thin": x["thin"],
                 "u4": site.u("4d/"), "zh": lang == "zh",
                 "mon": MON["en" if lang in ("en", "ta") else lang] if lang != "zh" else None}
            blob = json.dumps({"d": SD, "m": {n: mk(n) for n in sorted(shown) if mk(n)}, "l": L},
                              separators=(",", ":"), ensure_ascii=False)
            # Out of the HTML and into a hashed asset: the document stays small for the crawler
            # and for first paint, and this is cached for a year and never blocks anything.
            code = JS.replace("__P__", blob)
            name = f"assets/stf-{lang}." + hashlib.sha256(code.encode()).hexdigest()[:8] + ".js"
            (site.out / name).write_text(code, encoding="utf-8")
            return f'<script src="{site.u(name)}" defer></script>'

        # ---- provider filter: logo tiles, MKT first and selected by default ----
        SPR = {"M": 0, "T": 1, "D": 2, "S": 3, "C": 4, "H": 5, "G": 6, "N": 7, "J": 8, "K": 9}
        CO = {"M": "Magnum 4D", "D": "Da Ma Cai 1+3D", "T": "Sports Toto 4D", "G": "GD Lotto", "N": "9 Lotto",
              "S": "Singapore 4D", "C": "Sarawak Cash Sweep", "H": "Sandakan 4D"}
        if lang == "zh":
            CO = {"M": "万能", "D": "大马彩", "T": "多多", "G": "豪龙", "N": "9 Lotto",
                  "S": "新加坡万字", "C": "砂拉越大万", "H": "山打根"}
        WHO = dict(CO, mkt=x["mkt"], all=x["alln"], JK=x["jk"])

        def tile(fid):
            on = " on" if fid == DEF else ""
            if fid in ("mkt", "JK"):
                ks = "MDT" if fid == "mkt" else "JK"
                ic = "".join(f'<i style="background-position:-{SPR[k] * 21}px 0"></i>' for k in ks)
                return (f'<li><button type="button" class="fchip w multi{on}" data-f="{fid}" '
                        f'title="{esc(WHO[fid])}" aria-label="{esc(WHO[fid])}" aria-pressed="{str(not on == "").lower()}">{ic}</button></li>')
            if fid == "all":
                return (f'<li><button type="button" class="fchip w{on}" data-f="all" title="{esc(x["alln"])}" '
                        f'aria-label="{esc(x["alln"])}" aria-pressed="false">{esc(x["allco"])}</button></li>')
            return (f'<li><button type="button" class="fchip{on}" data-f="{fid}" title="{esc(CO[fid])}" '
                    f'aria-label="{esc(CO[fid])}" aria-pressed="false">'
                    f'<i style="background-position:-{SPR[fid] * 28}px 0"></i></button></li>')
        strip = (f'<div class="fw"><div class="flab">{esc(x["flab"])}</div>'
                 f'<div class="fstrip"><ul>' + "".join(tile(f) for f, _ in FILT) + '</ul></div></div>')
        scope = ('<p class="scope" id="scope">' + x["scope"].format(
            who=esc(WHO[DEF]), n=f"{A['nd']:,}", w=f"{A['total']:,}", u=f"{A['uniq']:,}") + '</p>')

        body = (f'<div class="st4">{lng}' + site.crumbs([(x["home"], pre), (x["crumb"], None)])[0]
                + f'<h1>{esc(x["h1"])}</h1><p class="lead">{esc(x["lead"].format(n=f"{NDALL:,}", s=S))}</p>'
                + strip + scope + f'{kp}{tabs}'
                + sec("hot", "🔥", x["hot"], x["hots"].format(s=S), f'<div class="card">{hot_h}</div>')
                + sec("cold", "❄️", x["cold"], x["colds"], f'<div class="card">{cold_h}</div>')
                + sec("recent", "📈", x["rec"], x["recs"].format(d=fd(d8(since90))), f'<div class="card">{rec_h}</div>')
                + sec("top3", "🏆", x["top"], x["tops"], f'<div class="card">{top_h}</div>')
                + sec("digits", "🔢", x["dig"], x["digs"], f'<div class="card" style="padding:12px">{hm}</div>')
                + sec("box", "🎲", x["box"], x["boxs"], bx)
                + f'<a class="cta" href="{site.u(pre + "?tab=check")}">{esc(x["more"])} ›</a>'
                + f'<a class="cta2" href="{site.u(pre + "popular-4d-numbers/")}">{esc(x["pop"])} ›</a><div class="nt">{esc(x["note"])}</div></div>'
                + fscript())
        bc, bld = site.crumbs([(x["home"], pre), (x["crumb"], None)])
        ds = {"@context": "https://schema.org", "@type": "Dataset", "name": x["title"], "description": x["desc"].format(n=f"{NDALL:,}", s=S), "inLanguage": hl,
              "temporalCoverage": f"{d8(s0).isoformat()}/{last.isoformat()}", "creator": {"@type": "Organization", "name": "4D Malam Ini"}}
        site.page(path(lang), x["title"] + " | 4D Malam Ini", x["desc"].format(n=f"{NDALL:,}", s=S), body, lang=hl, ld=[bld, ds],
                  head=f'<link rel="stylesheet" href="{site.u(css_name)}">' + alts, lastmod=last.isoformat())
