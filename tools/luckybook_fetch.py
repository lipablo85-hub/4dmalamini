"""One-off: pull the 4D Lucky Book dictionaries (4dluckybook.com) into luckybook/.
Pages through /home/bookitemlist?id=N&offset=K (20 per page), parses number + text, downloads each image,
re-encodes it as WebP (q90, original size) to keep the data branch small. Writes luckybook/book<N>.json."""
import html, json, re, sys, time, urllib.request
from io import BytesIO
from pathlib import Path
from PIL import Image

B = "https://4dluckybook.com"
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36", "Referer": B + "/home/"}
out = Path(sys.argv[1]); out.mkdir(exist_ok=True)

def get(u, tries=4):
    for t in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
        except Exception as e:
            err = e; time.sleep(2 + 3 * t)
    raise err

ITEM = re.compile(r"""<img id="bookitemitemphoto"\s+src='([^']+)'\s*alt="([^"]*)".*?<div id="bookitemitemname"><b>([^<]*)</b>""", re.S)
for bid in sys.argv[2:]:
    first = get(f"{B}/home/?menu=bookitem&id={bid}").decode("utf-8", "replace")
    (out / f"page{bid}.html").write_text(first)
    title = re.search(r'id="bookitemtitle[^>]*>(.*?)<', first, re.S)
    items, seen, off, pages = [], set(), 0, [first]
    while True:
        frag = first if off == 0 else get(f"{B}/home/bookitemlist?id={bid}&offset={off}").decode("utf-8", "replace")
        got = ITEM.findall(frag)
        new = [g for g in got if g[0] not in seen]
        if not new:
            break
        for src, alt, num in new:
            seen.add(src)
            desc = html.unescape(alt.split(" - ", 1)[1] if " - " in alt else alt)
            lines = [l.strip() for l in desc.split("\n") if l.strip()]
            items.append({"n": num.strip(), "src": src, "lines": lines})
        off += 20
        time.sleep(0.15)
    (out / f"img{bid}").mkdir(exist_ok=True)
    dims, fails = {}, []
    from concurrent.futures import ThreadPoolExecutor
    def one(i_it):
        i, it = i_it
        try:
            im = Image.open(BytesIO(get(it["src"].replace("http://", "https://"))))
            im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
            name = f"{it['n']}.webp" if i == firsts[it["n"]] else f"{it['n']}-{i}.webp"
            im.save(out / f"img{bid}" / name, "WEBP", quality=90, method=5)
            return i, name, im.size, None
        except Exception as e:
            return i, None, None, str(e)[:80]
    firsts = {}
    for i, it in enumerate(items):
        firsts.setdefault(it["n"], i)
    with ThreadPoolExecutor(6) as ex:
        for i, name, size, err in ex.map(one, enumerate(items)):
            if err:
                fails.append((items[i]["n"], err))
            else:
                items[i]["img"] = name; dims[size] = dims.get(size, 0) + 1
    json.dump({"id": bid, "title": title.group(1).strip() if title else "", "items": items}, open(out / f"book{bid}.json", "w"), ensure_ascii=False, indent=0)
    nums = [it["n"] for it in items]
    print(f"book {bid}: {len(items)} items, numbers {nums[:3]}..{nums[-3:]}, dup numbers {len(nums) - len(set(nums))}, "
          f"image sizes {sorted(dims.items(), key=lambda x: -x[1])[:4]}, failed {len(fails)} {fails[:5]}", flush=True)
