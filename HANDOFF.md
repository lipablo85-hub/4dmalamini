# 4D Malam Ini — handoff

Everything a fresh session needs to work on **www.4dmalamini.com**. Written 5 Nov 2026.

---

## 1. What it is

A mobile-first Malaysian 4D results site in four languages (EN / BM / 中文 / தமிழ்).
Static site generator → Cloudflare Pages. 12,181 prerendered HTML pages, no framework,
no server. The home page is a single-page app that polls a Cloudflare Function for live
results; everything else is prerendered HTML.

| | |
|---|---|
| Live | https://www.4dmalamini.com |
| Repo | `lipablo85-hub/4dmalamini` (GitHub) |
| Host | Cloudflare Pages, deployed by GitHub Actions on push to `main` |
| Owner | Site owner, timezone MYT (UTC+08:00) |

**Eleven operators**, keyed by a single letter throughout the codebase:

| Key | Operator | Rows | Draw time (DRAWM) |
|---|---|---|---|
| `M` | Magnum 4D | 841 | 7:00pm |
| `D` | Da Ma Cai 1+3D | 841 | 7:00pm |
| `T` | Sports Toto 4D | 841 | 7:00pm |
| `G` | GD Lotto 4D | 1,829 | 7:00pm |
| `N` | 9 Lotto 4D | 221 | 7:00pm (started 29 Mar 2026) |
| `S` | Singapore 4D | 777 | 6:30pm |
| `C` | Sarawak Cash Sweep | 825 | 7:00pm |
| `B` | Sabah 88 4D (Diriwan) | 840 | 7:00pm (added 5 Nov 2026) |
| `H` | Sandakan 4D | 840 | 7:00pm |
| `J` | Super J3 3PM | 18 | 3:00pm |
| `K` | Super J9 9PM | 17 | 9:00pm |

7,890+ draws total. Display order everywhere: … Cash Sweep → Sabah 88 → Sandakan (user's rule). **MKT** is the user's shorthand for Magnum + Da Ma Cai + Sports Toto —
the "big three" that draw Wed/Sat/Sun plus special draws.

---

## 2. Standing preferences (from the user)

- **"Always look for innovative, expert results."**
- **"Any web design or graphic design always streamline the size with optimized size and loads."**
  Page weight is a real constraint, not a nicety. Measure it; don't estimate.
- **Draft a visual before deploying any new design.** The established pattern is: build a
  working HTML draft with real data, publish it as an artifact, wait for approval, then build
  it for real. The user often picks between labelled options (A / B / C).
- Mobile-first. The site's pitch is being the fastest way to check a result.
- The user reviews carefully and spots misalignment. Check your own screenshots before
  presenting them.

---

## 3. Security constraints — do not break these

- **Never paste any API token in chat.** Tokens live only as GitHub repo secrets and are
  read inside workflows as `${{ secrets.NAME }}`.
- Secrets currently set: `CLOUDFLARE_API_TOKEN` (Pages deploy), `DISPATCH_TOKEN`
  (lets `/api/live` trigger `results.yml`), `CF_ZONE_TOKEN` (Zone → Single Redirect: Edit,
  scoped to this zone only — created 5 Nov for the redirect fix; safe to delete).
- The user's email is for identification only. Never send it to a third-party service.

---

## 4. Build and test

```bash
# full build (~2 min, writes 12k files)
python3 tools/build.py \
  --results malaysia_4d_draws_2021-2026.csv \
  --dict 4d_dictionary_template.csv \
  --img-src sprites --text dict_text \
  --site https://www.4dmalamini.com/ --out /tmp/sd1
```

Local preview server (the helper lives at `/tmp/gz9.py` in past sessions; any static server
with gzip works). Pick a fresh port each time:

```bash
sed 's/8769/8790/' /tmp/gz9.py > /tmp/gz_new.py
(python3 -I /tmp/gz_new.py /tmp/sd1 &)
```

> **Never run `pkill -f gz9.py`.** The pattern matches the agent's own command line and kills
> the shell. Just use a new port.

Playwright is available for screenshots, interaction tests and Core Web Vitals
(`PerformanceObserver` for CLS/LCP, `clock.install()` to fake draw times, route mocks for
`/api/live`).

---

## 5. File map

```
tools/
  build.py            orchestrator; home SPA prerender per language, _headers, assets,
                      IndexNow key file, calls every *_pages.py module
  page.template.html  the home SPA — markup + CSS + JS in one file. The biggest file.
  seo_pages.py        Site class (loads results + dictionary), date pages, number pages,
                      year/month archive silos, localize(), crumbs(), sitemap index
  seo_copy.py         the per-language SEO prose block on the home page
  op_pages.py         operator hubs (/magnum-4d-result/) + provider-year archives
  stats_pages.py      /4d-statistics/ incl. the provider filter
  popular_pages.py    /popular-4d-numbers/
  special_pages.py    /special-draw/
  check_pages.py      /check-4d-number/
  legal_pages.py      /privacy/ /terms/ /contact/
  about_pages.py      /about/   info_pages.py /info/   guide_pages.py /guide/
  sitemap_pages.py    the HTML sitemap at /sitemap/
  fetch_results.py    scrapes check4d + loto4d for nightly results
  backfill_*.py       one-off history backfills
  brand/op/tk.webp    10 operator logos in one 400×40 sprite (served /img/op/tk.webp)

malaysia_4d_draws_2021-2026.csv   the single source of truth for results
4d_dictionary_template.csv        4D dictionary (万字图) base
dict_text/                        per-number meanings, 4 languages, 10,000 entries
sprites/                          dictionary images

functions/api/live.js   Cloudflare Function: live results + auto-save dispatch
.github/workflows/      deploy.yml  results.yml  backfill.yml  check.yml
```

### URL structure

```
/  /ms/  /zh/  /ta/              home SPA per language
/keputusan/                      archive hub  (Malay namespace, no prefix)
/keputusan/2026/                 year hub
/keputusan/2026/11/              month silo
/keputusan/2026-11-04/           date page          ← indexed, never move these
/4d/8888/                        number page        ← Malay namespace
/4d/0000-0999/                   dictionary range
/{lang}/magnum-4d-result/        operator hub
/{lang}/magnum-4d-result/2025/   provider-year archive
/{lang}/4d-statistics/ popular-4d-numbers/ check-4d-number/ special-draw/
/{lang}/info/ guide/ about/ sitemap/ privacy/ terms/ contact/
/data-policy/                    single-language, shared
```

---

## 6. Gotchas that cost real time — read before editing

**Language routing.** `/keputusan/…` and `/4d/…` are the **Malay** namespace with no prefix.
`seo_pages.localize()` rewrites links per language: for non-Malay pages a date link becomes
`?d=YYYYMMDD` and a number link `?n=NNNN`. Two traps:
- `localize()` has an early return for `lang == "ms"` so it doesn't rewrite Malay pages. The
  `MSROOT` regex is the exception list of section roots that still need the `/ms/` prefix.
- **Anything JSON-encoded is invisible to `localize()`** because the quotes are escaped. The
  home footer ships all four language variants as a JSON blob (`FLINKS`) for the in-page
  language switcher; each variant must be passed through `SP.localize()` *before* encoding.
  This bug shipped once — English users got Malay pages from the footer.

**Audit links in a browser, not by reading HTML.** The home page builds much of itself in JS,
so a regex over the server-rendered markup misses the real DOM. The working audit loads each
language, switches language in-page, opens the tabs, and checks every *visible* link
(`offsetParent !== null`); hidden elements produce false positives — the per-language SEO
prose block is `hidden` rather than translated on switch.

**Cloudflare Pages `_headers` does not override — it JOINS.** A request matching several rules
inherits all of them, and a repeated header is concatenated with a comma. A `/*` baseline plus
per-path overrides produces `Cache-Control: max-age=0, must-revalidate, public, max-age=600…`.
Rules must be **non-overlapping**; `/*` carries security headers only.

**`cf-cache-status: DYNAMIC` on HTML is normal**, not a misconfiguration — it's Cloudflare's
documented default for HTML. Don't "fix" it without a Cache Rule; measure TTFB first.

**GitHub Actions**
- `gh workflow run` fails (no GraphQL access). Use
  `gh api -X POST repos/OWNER/REPO/actions/workflows/FILE/dispatches -f ref=main`.
- Inline Python inside a `run: |` block must stay indented. A line at column 0 terminates the
  YAML literal block, the workflow silently becomes invalid, and dispatch then fails with
  *"Workflow does not have 'workflow_dispatch' trigger"*. Prefer `jq`. Validate with
  `python3 -c "import yaml;yaml.safe_load(open(...))"` before pushing.
- The queue backs up for 20–40 minutes sometimes. Not a code problem; poll patiently.

**The sandbox cannot reach the live site.** Outbound HTTPS to 4dmalamini.com / loto4d /
check4d is blocked and WebFetch rejects non-allowlisted hosts. To check anything live, write
the checks into `.github/workflows/check.yml`, dispatch it, and read the log. That file is a
scratch probe — rewrite it freely.

**iOS 26 Safari ignores `theme-color`.** It tints its top/bottom bars from the sticky header and
the fixed bottom nav (or the body background), and a `backdrop-filter` on those bars stops the
sampling. Keep both bars solid theme colour with no blur (`themes.INLINE_CSS_TAIL`).

**Verify every scripted edit.** A heredoc that does all its `s.replace()` work then writes at
the end will silently write nothing if an assertion fails partway. `grep` after each edit.

**Push routine**

```bash
git stash -q; git pull -q --rebase origin main; git stash pop -q
git push -q origin HEAD:main
```

Commit messages end with the attribution trailer the session's system-reminder specifies —
read it from the current session, it changes.

---

## 7. Current state (5 Nov 2026)

**Audit, all 12,181 pages:** 0 duplicate titles or descriptions, 0 over-length titles (>70) or
descriptions (>160), 0 broken internal links, 0 cross-language links, 0 orphan pages, 0 pages
missing from the sitemap, 26,226 JSON-LD blocks valid, hreflang fully reciprocal.

**Performance:** CLS 0, LCP 112–268 ms across page types. Home SPA HTML ~28 KB gz (6 Nov: the
~100 KB app script moved to `assets/app.<hash>.js`, `defer` in `<head>`, identical for all four
languages and cached forever); date pages ~6 KB gz; statistics 6 KB gz + a 12 KB deferred filter asset.

**Themes (6 Nov, `tools/themes.py` + `tools/theme_sky.py`):** header switch Black (default) /
Day / Starry Night on the four home pages. `themes.apply()` runs on the minified home HTML and
turns every role colour into a CSS variable (`ROLE` map: base shade -> role; palettes per theme),
SVG/meta attributes excluded. Day needs extra overrides (`DAY_FIX`). The Van Gogh sky is NOT in
the page: `assets/sky.<hash>.txt` (not .html: Pages redirects those) (~8 KB gz) is fetched only when Starry Night is active.
Choice kept in `localStorage.th`. GA4: user property `ui_theme` (set before `config`, so the first
page_view carries it) + event `theme_select {theme, theme_from}`; the user must register both as
custom dimensions in GA Admin. Static SEO/info pages are not themed yet (still navy).
If the home template's colours change, re-check `ROLE` covers the new shades.

**Caching** (`_headers`): archive 10 min + 1 day SWR, dictionary and provider-year 1 day +
7 day SWR, assets 1 year immutable, home and operator hubs `must-revalidate` (they show
tonight's draw), `/live.json` `no-store`.

**Redirects:** every entry point is one hop. The apex rule matches `http.host` so it catches
HTTP and HTTPS in one pass. HSTS is **off** — a deliberate open choice, not an oversight.

**Indexing:** sitemap *index* split into main / results / operators / dictionary so Search
Console reports per section. IndexNow fires on every deploy (Bing/Yandex). **Google's Indexing
API is deliberately not used** — it is documented as supported only for `JobPosting` and
`BroadcastEvent`, and using it for result pages risks revocation.

**Schema:** Dataset + BreadcrumbList + ItemList on date pages, ItemList on month/year hubs,
FAQPage on several (note: Google **retired the FAQ rich result on 7 May 2026** — the markup
is kept for machine comprehension, but it will not change the SERP).

**Known data gaps:** 24 (operator, date) pairs are genuinely unpublished by both sources —
Cash Sweep 16 (23 Aug–24 Sep 2023), Singapore 7 (Jul–Aug 2025), Sandakan 1 (20 Mar 2024), Sabah 88 1 (16 Nov 2024).
Backups: git tags `data-20261104-1859`, `data-20261104-1939`.

### Shipped 5 Nov
Year/month archive silos · provider-year pages · 5-level breadcrumbs · provider H2s on date
pages · ItemList schema · footer follows language · number-search hub · sitemap index ·
freshness lines + `dateModified` · privacy/terms/contact · cache headers · one-hop redirect ·
desktop footer and sheet alignment · provider filter on the statistics page · heat map caption (option A: real spread, 4 languages).
Home header logo intro (option D, "Van Gogh cloud"): SVG + CSS in `page.template.html`, +1.3 KB gz, plays once
(~2.9 s) then the old twinkle loop. Finished logo is the default; intro only under `prefers-reduced-motion: no-preference`.
Draft sources in the artifact "4D Malam Ini: logo intro D" (A-C in its earlier versions). Inner pages keep the static `mark.svg`.
Sabah 88 4D (key `B`, slug `sabah-88-4d-result`): 840 draws from check4d cross-checked with 4d2ulive (0 conflicts); draw 3950
(16 Nov 2024) unpublished by both. Logo sprite is now `img/op/tk11.webp` (11 tiles; `/img/*` is immutable, so a new sprite
needs a new file name). Ticker sprite positions come from the `TKI` map, not display order. Temp branch `sabah88-data` can be deleted.
Dictionary has three books (6 Nov): 4D Dream Numbers = the existing 10,000 (`dict_text/`, `sprites/`), Tua Pek Kong and
Guan Yin Ma 000-999 from 4D Lucky Book (`dict_books/tpk.json`, `gy.json`, `sprites_tpk/`, `sprites_gy/`, 200 px AVIF sheets made by
`tools/book_img.py`; owner states the images are free to use). Lucky Book's 万字图 is the same drawings as ours at half the
resolution, so only its extra wordings are kept (`dict_books/wz_alt.json`, 8th search-only field in each dict chunk). One search
covers all three; a 4-digit number matches the 3-digit books on its last 3 digits. Header results strip: Results tab only.
Temp branch `luckybook-data` (raw pull, 221 MB) can be deleted.

### Open
- **HSTS** — user's decision, not started. Start at `max-age=86400`, no `includeSubDomains`,
  no `preload`. Hard to undo; see the reasoning in the session history.
- **Possible data errors (not yet checked against a source).** Chi-square tests on digit-by-position
  counts show two anomalies that start or stop at a date, which points at the data rather than the draws:
  Sandakan digit 4 is 12-15% of digits every month since Mar 2026 (16-17% in 1st-3rd prize; 10% is even);
  Magnum digit 7 is ~1 point low in each of 2022-2025, normal in 2026. Verify a sample against check4d and
  loto4d via `check.yml` before trusting either. No duplicate draws or malformed numbers were found.
- Filling the 24 data gaps needs a source neither check4d nor loto4d has.
- `CF_ZONE_TOKEN` can be deleted now that the redirect is fixed.

---

## 8. How to start the next session

1. Attach the repo: `mcp__claude-code-remote__add_repo` with owner `lipablo85-hub`,
   repo `4dmalamini`, then clone and `register_repo_root`.
2. Read this file and `README.md`.
3. Build once to `/tmp/` and confirm 12,181 pages with no errors before changing anything.
4. For anything visual, draft → artifact → approval → build → deploy → verify live via
   `check.yml`.
