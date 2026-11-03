// GET /api/live : numbers drawn so far tonight (partial while a draw is in progress).
// Reads check4d.org (Magnum, Da Ma Cai, Sports Toto, GD) and loto4d.com (9 Lotto, GD backup); cached 15 s at the edge.
const SRC = { c4d: "https://www.check4d.org/", loto: "https://loto4d.com/" };
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36";

const text = h => h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, " ").replace(/<[^>]+>/g, " ")
  .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&#\d+;/g, " ").replace(/\s+/g, " ");

function block(t, title, ends) {
  const i = t.indexOf(title); if (i < 0) return null;
  let j = t.length;
  for (const e of ends) { const k = t.indexOf(e, i + title.length); if (k > 0 && k < j) j = k; }
  return t.slice(i, j);
}
const TOK = /\d{4}|-{4}|\*{4}/g;
function parse(b) {
  if (!b) return null;
  const dm = b.match(/Date:\s*(\d{2})-(\d{2})-(\d{4})/); if (!dm) return null;
  const no = (b.match(/Draw No:\s*([\d/]+)/) || [])[1] || "";
  const top = [1, 2, 3].map(i => { const m = b.match(new RegExp(["1st", "2nd", "3rd"][i - 1] + "(?: Prize)? \\S+ (\\d{4}|-{4}|\\*{4})")); return m && /\d/.test(m[1]) ? m[1] : ""; });
  const sp = b.match(/Special(.*?)Consolation/); const co = b.match(/Consolation(.*)$/);
  const sl = sp ? (sp[1].match(TOK) || []).map(x => /\d/.test(x) ? x : "") : [];
  const cn = co ? (co[1].match(TOK) || []).slice(0, 10).map(x => /\d/.test(x) ? x : "") : [];
  return { d: dm[3] + dm[2] + dm[1], no, top, sl, co: cn };
}
async function grab(url, ctx) {
  const cache = caches.default, key = new Request(url + "#live");
  let r = await cache.match(key);
  if (!r) {
    const up = await fetch(url, { headers: { "User-Agent": UA, Referer: url }, cf: { cacheTtl: 0 } });
    if (!up.ok) return "";
    r = new Response(await up.text(), { headers: { "Cache-Control": "max-age=15" } });
    ctx.waitUntil(cache.put(key, r.clone()));
  }
  return text(await r.text());
}
async function jgrab(ctx) {
  const url = "https://superj3.net/data/data-api.php?op=get_landing_info&api_key=e0a5d3fsdfdsghhg18b0c8bgfdgd7c06e&ao=1";
  const cache = caches.default, key = new Request(url + "#live");
  let r = await cache.match(key);
  if (!r) {
    const up = await fetch(url, { headers: { "User-Agent": UA, Referer: "https://superj3.net/" } });
    if (!up.ok) return null;
    r = new Response(await up.text(), { headers: { "Cache-Control": "max-age=15" } });
    ctx.waitUntil(cache.put(key, r.clone()));
  }
  return JSON.parse(await r.text());
}
export async function onRequestGet(ctx) {
  const out = { t: Date.now(), ops: {} };
  const [c, l] = await Promise.all([grab(SRC.c4d, ctx).catch(() => ""), grab(SRC.loto, ctx).catch(() => "")]);
  const E = ["Advertisements", "Da Ma Cai 1+3D", "SportsToto 4D", "SportsToto 5D", "Da Ma Cai 3+3D", "Magnum Life", "Grand Dragon", "Perdana", "Lucky HariHari", "Nine Lotto", "Magnum 4D", "SINGAPORE", "Sandakan", "4D Jackpot 1 Prize", "-->"];
  const put = (k, v) => { if (v && (!out.ops[k] || v.d > out.ops[k].d)) out.ops[k] = v; };
  if (c) {
    put("M", parse(block(c, "Magnum 4D 萬能", E)));
    put("D", parse(block(c, "Da Ma Cai 1+3D", E)));
    put("T", parse(block(c, "SportsToto 4D", E)));
    put("G", parse(block(c, "Grand Dragon 4D", E)));
  }
  if (l) {
    put("G", parse(block(l, "Grand Dragon 4D", E)));
    put("9", parse(block(l, "Nine Lotto Date", E)));
  }
  // Super J3 (3pm) / J9 (9pm): superj3.net JSON feed (key is public, embedded in their page)
  try {
    const r = await jgrab(ctx);
    const lr = (r && r.last_result) || {};
    for (const [id, v] of Object.entries(lr)) {
      if (!v || typeof v !== "object" || !v.DATE) continue;
      const k = v.dt === "15" || v.TIME === "3PM" ? "J" : "K";
      const cell = x => /^\d{4}$/.test(x || "") ? x : "";
      put(k, { d: v.DATE.slice(0, 10).replace(/-/g, ""), no: "", top: [v.FIRST, v.SECOND, v.THIRD].map(cell),
               sl: Object.values(v.SP || {}).map(cell), co: Object.values(v.CS || {}).map(cell) });
    }
  } catch (e) {}
  return new Response(JSON.stringify(out), { headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=15" } });
}
