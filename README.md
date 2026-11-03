# 4D Malam Ini (4dmalamini.com): site package

## Why the live site said "Could not load results"
The page loaded, but `data/results.e6e293da.json` did not, so the `data/` folder is missing or incomplete on Netlify.
Netlify drag-and-drop often drops files when a folder has tens of thousands of them (the pictures).
Check: open https://4dmalamini.com/data/results.e6e293da.json. A 404 means the data was not uploaded.
The fix is option B below (Netlify builds the site itself from GitHub).

## Option A: quick drag-and-drop (no nightly updates)
Unzip `4dmalamini-site.zip` and drag the whole folder onto Netlify → Deploys. Then open the data link above to confirm it loads.

## Option B: GitHub + Netlify (recommended, results update by themselves every night)
1. Create a new GitHub repository (private is fine) and upload everything from `4dmalamini-source.zip`,
   including the hidden `.github` folder (GitHub Desktop or `git push` keeps it; the web uploader may skip it).
2. Netlify → your site → Site configuration → Build & deploy → Link repository → pick the repo.
   `netlify.toml` already sets the build command and the `dist` publish folder.
3. GitHub → repo → Actions → enable workflows. "Nightly 4D results" then runs every 5 minutes from 7:00 to 8:55 pm
   (plus 9:30 and 11:30 pm), saves new complete draws to the CSV, and Netlify republishes in 1-2 minutes.
   Run it once by hand: Actions → Nightly 4D results → Run workflow. The log should say "no complete result" on non-draw days.
4. If the log shows "Sports Toto 4D: could not fetch", the Toto site is blocking GitHub's servers. Tell me and I'll add a backup source.

GitHub can start scheduled runs a few minutes late at busy times. Results usually appear on the site by about 8:15-8:30 pm.

## SEO and speed (this build)
Lighthouse (mobile, slow-phone simulation): home 92-98 performance, 100 SEO / accessibility / best practices;
number, result and dictionary pages 100 in every category. No layout shift (was 0.39), page freeze 150 ms (was 1,050 ms).

Pages Google can now index:
- `/`, `/ms/`, `/zh/`, `/ta/`: the app pre-filled in each language, linked with hreflang. Switching language updates the address.
- `/4d/0000/` … `/4d/9999/`: one page per number with picture, 4-language meaning, full win history and Box links.
- `/keputusan/YYYY-MM-DD/`: full results per draw date (840 so far, a new one after every draw).
- `/4d/` and `/4d/0000-0999/` … hubs, `/keputusan/` archive, `sitemap.xml` (10,856 URLs), `robots.txt`, branded `404.html`.
- Structured data: WebSite with search box, Organization, and breadcrumbs on every static page.

After launch:
1. In Netlify → Domain management, make **www.4dmalamini.com** the primary domain (4dmalamini.com redirects to it). The build uses www everywhere.
2. Google Search Console → add www.4dmalamini.com → Sitemaps → submit `sitemap.xml`.
3. Optional: Bing Webmaster Tools → import from Search Console.

## What's new in this build
- Brand: 4D Malam Ini logo in the header, navy/cream/gold colours, favicon, app icons (incl. Android maskable), and a share preview image (`og-image.jpg`) for WhatsApp and Facebook.
- Dictionary: all 10,000 entries have Chinese, English, Bahasa Melayu and Tamil text, so word search works in all four languages.
  328 uncertain readings are listed in `to_review.csv`; fix them in `dict_text/NNNN.tsv` and push.
- Pictures: AVIF format, 4 KB per grid picture (was 13 KB), 7 KB enlarged, WebP backup for older phones.
- Dictionary text loads in 10 small pieces (about 33 KB each) only when needed.
- If results fail to load, the latest results stay visible with a Retry button.

## Upload
Upload everything inside `dist/` to your web folder (e.g. `public_html/4d/`). Keep the folder structure.

| File | What it is | Size (gzip) |
|---|---|---|
| `index.html` | The page: EN / BM / 中文 / தமிழ், with English text and last night's results built in so they show on the first frame | ~15 KB |
| `data/results.<hash>.json` | 5 years of Magnum, Sports Toto, Da Ma Cai (2,520 draws). Downloads in the background, cached for a year | ~127 KB |
| `data/dict.<hash>.txt` | Dictionary meanings (only created once the template has content). Loads only when the Dictionary tab opens | — |
| `sw.js` | Offline support + instant repeat visits (works on https only) | <1 KB |
| `manifest.webmanifest`, `icon*.png`, `icon.svg` | "Add to Home Screen" app icon | ~8 KB |
| `.htaccess` (Apache / cPanel) or `_headers` (Netlify / Cloudflare Pages) | Compression + cache rules | — |

Measured on a simulated slow 4G phone (4× slower CPU), gzip on: last night's results visible in ~0.6 s (previous single-file version: ~1.3 s); fully interactive in ~1.3 s.

## Automatic results every night, 7–9 pm (recommended)
`tools/fetch_results.py` runs on your web server, reads tonight's results straight from the official
Magnum, Sports Toto and Da Ma Cai websites, adds complete draws to the CSV and rebuilds the site.
Standard Python 3 only, nothing to install.

1. Upload this whole package (not only `dist/`) to a folder on the server, e.g. `/home/USER/4d/`.
2. Copy `dist/img/dict` to `enhanced/` (picture source for rebuilds).
3. Point your domain or sub-folder at `/home/USER/4d/dist` (cPanel: domain document root, or a symlink
   `ln -s /home/USER/4d/dist /home/USER/public_html/4d`).
4. Test once by hand (fetches a past night, changes nothing):
   ```
   cd /home/USER/4d && python3 tools/fetch_results.py --csv malaysia_4d_draws_2021-2026.csv --date 2026-11-01 --dry-run
   ```
5. Add the cron job (cPanel → Cron Jobs). Every 5 minutes from 7:00 to 8:55 pm Malaysia time, plus 9:30 and 11:30 pm catch-ups:
   - Server clock on **Malaysia time**: `*/5 19-20 * * *` and `30 21,23 * * *`
   - Server clock on **UTC** (most hosts): `*/5 11-12 * * *` and `30 13,15 * * *`

   Command (one line):
   ```
   cd /home/USER/4d && python3 tools/fetch_results.py --csv malaysia_4d_draws_2021-2026.csv --dist dist --build "python3 tools/build.py --results malaysia_4d_draws_2021-2026.csv --dict 4d_dictionary_template.csv --img-src sprites --site https://yourdomain.com/4d/ --out dist.new" >> fetch.log 2>&1
   ```
   Check your server clock with `date` in the terminal.

What it does each run: skips companies already saved for tonight; saves a draw only when all 23 numbers are
out (partial live results wait for the next run); never overwrites a saved draw (logs `CONFLICT` if a site
later shows different numbers); rebuilds into `dist.new` and swaps it in at once. Non-draw days just log
"no complete result". Check `fetch.log` after the first draw night.

If the Sports Toto site blocks your server (some block data-centre IPs), the log will show
"Sports Toto 4D: could not fetch". Tell me and I'll add a backup source.

## Update by hand (if needed)
1. Add the new draw rows to `malaysia_4d_draws_2021-2026.csv` (same columns).
2. Run:
   ```
   npm i -g html-minifier-terser      # once
   python3 tools/build.py --results malaysia_4d_draws_2021-2026.csv --dict 4d_dictionary_template.csv --img-src sprites/ --site https://yourdomain.com/4d/
   ```
3. Upload the new `dist/` folder. The data file gets a new name whenever it changes, so visitors never see old results. Old `data/results.*.json` files can be deleted after upload.

The build stops with a clear message if a row has a bad date, a number that is not 4 digits, or a duplicate draw.

## Dictionary pictures included
`dist/img/dict/` holds **All 10,000 enhanced pictures (0000–9999)**: 400×400 WebP, average 13 KB, about 126 MB total.
They load only as visitors scroll (about 30 at a time). Every range 0000–9999 is complete.until their pictures are added.
To add more: put the original `NNNN.jpg` files in a folder, then
```
python3 tools/wzt_img.py originals/ enhanced/
python3 tools/build.py --results malaysia_4d_draws_2021-2026.csv --dict 4d_dictionary_template.csv --img-src sprites/ --site https://yourdomain.com/4d/
```
Before your first rebuild, copy `dist/img/dict` to `enhanced/` (the build replaces `dist/`). Keep your written permission for these pictures on file.

## Dictionary (0000–9999)
- Fill `4d_dictionary_template.csv`: `category`, `chinese_中文`, `english`, `malay_bahasa_melayu`, `tamil_தமிழ்`. The `image_file` column is pre-filled (`img/dict/0001` etc.).
- Pictures: put originals named by number (`0001.jpg`, `1.jpg` or `wzt_0001.png` all become 0001) in a folder and run
  ```
  python3 tools/dict_img.py photos/ dist/img/dict/ --motion
  ```
  → 4:3 enhanced AVIF + WebP in two sizes, blur previews, and a 4-second moving loop (MP4, ~100 KB) per picture.
- Use only pictures you own or are licensed to use.

## Files
- `tools/page.template.html`: source of the page (edit text/design here, then rebuild)
- `tools/build.py`: builds `dist/`
- `tools/dict_img.py`: picture enhancer / optimiser
- `malaysia_4d_draws_2021-2026.csv`: results data (sources: public archives cross-checked; Sports Toto 25–31 Oct 2026 from sportstoto.com.my)
- `4d_dictionary_template.csv`: 10,000-row dictionary template

Set your real address in `--site` (used for the canonical link and share previews).

## Guide pages (how to play)
`tools/guide_pages.py` writes `/guide/` (+ `/ms/guide/`, `/zh/guide/`, `/ta/guide/`) and one page per company
(`magnum-4d/`, `sports-toto-4d/`, `da-ma-cai-1-3d/`). All text lives in that file, in 4 languages.

## Page weight
The home page first loads only `live.json` (last few draws, ~1 KB). The 5-year history file loads when a visitor
checks a number, opens past draws or steps back through dates (and starts loading as soon as they tap those controls).

## Cloudflare Pages (recommended host)
The site has about 11,700 files (pages + 800 picture sheets), under Cloudflare's 20,000-file limit.
The dashboard drag-and-drop accepts only 1,000 files / 25 MiB, so deploy from GitHub with Wrangler:

1. Push this folder to a GitHub repo (branch `main`). GitHub Desktop is easiest for the ~1,400 files.
2. Cloudflare dashboard -> My Profile -> API Tokens -> Create Token -> "Edit Cloudflare Workers" template
   (or a custom token with Account > Cloudflare Pages > Edit). Copy your Account ID from the Workers & Pages overview.
3. GitHub repo -> Settings -> Secrets and variables -> Actions -> add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.
4. Actions -> "Deploy site" -> Run workflow. The first run creates the Pages project "4dmalamini" and publishes it.
5. Workers & Pages -> 4dmalamini -> Custom domains -> add www.4dmalamini.com (and 4dmalamini.com).
Every night the results workflow commits new draws and redeploys automatically.

## Dictionary pictures
`tools/sprite_img.py --src enhanced --out sprites` packs the 10,000 pictures into 400 sheets per size (25 per file).
Only `sprites/` is needed in the repo; the original `enhanced/` folder can stay on your computer.
