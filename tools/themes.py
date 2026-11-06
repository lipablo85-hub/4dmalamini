"""Colour themes for the home app: Black (default), Day and Starry Night, with a header switch.

Run on the built home pages (after minifying). Every themed colour in the page becomes a CSS
variable, so the three themes cost ~1.5 KB of variables instead of three stylesheets.
The Starry Night painting is NOT in the page: it is a separate fingerprinted fragment
(assets/sky.<hash>.txt, cached forever) fetched only when a visitor picks Starry Night, so
Black and Day visitors never download it.
GA4: user property ui_theme on every hit (queued before gtag config, so the first page_view has
it) and a theme_select event {theme, theme_from} on each button press.
"""
import hashlib, re
from pathlib import Path
import theme_sky as sky

# shade in the base page -> role; each theme gives every role a colour
ROLE = {"#07142b": "bg", "#0f1f3d": "surf", "#172a4d": "raise", "#233862": "bord", "#1a2c50": "line", "#1d3157": "line2",
        "#a9b4cc": "mut", "#9db0d3": "mut", "#9fb0d3": "mut", "#7f90b3": "mut2", "#7c89a6": "mut2", "#c9d1de": "sub", "#c9d4ea": "sub", "#e4eaf6": "sub",
        "#f8f4e8": "ink", "#e9c46b": "acc", "#1b1300": "onacc", "#1a1405": "onacc", "#5a4630": "bar", "#cfc5b5": "cellb", "#f4efe6": "cellf",
        "#050e22": "bg", "#0a1730": "bg", "#0a1733": "bg", "#0b1934": "bg", "#0e1d3b": "surf", "#0e1e3d": "surf", "#13254a": "surf", "#16294f": "surf", "#1a2747": "surf",
        "#1e3361": "raise", "#1c3567": "raise", "#1e3a6b": "raise", "#203a6b": "raise", "#2a3e66": "bord"}
T = {
 "A": {"bg": "#0B0F1A", "surf": "#141A2A", "raise": "#1B2236", "bord": "#2A3350", "line": "#20283D", "line2": "#252E46", "mut": "#9AA3B8", "mut2": "#7E879C",
       "sub": "#CDD3DF", "ink": "#F3F1EA", "acc": "#D9B45A", "onacc": "#17120A", "bar": "#232B3F", "cellb": "#D9DEE7", "cellf": "#F2F4F8", "rgb_bg": "11,15,26", "rgb_acc": "217,180,90", "rgb_ink": "243,241,234"},
 "B": {"bg": "#F3EFE6", "surf": "#FFFFFF", "raise": "#F8F4EB", "bord": "#E2DACB", "line": "#E8E1D3", "line2": "#E2DACB", "mut": "#6B6457", "mut2": "#8A8273",
       "sub": "#3D382F", "ink": "#1C1A16", "acc": "#8F6400", "onacc": "#FFFFFF", "bar": "#2E2A24", "cellb": "#E2DACB", "cellf": "#FAF7F0", "rgb_bg": "243,239,230", "rgb_acc": "143,100,0", "rgb_ink": "28,26,22"},
 "C": {"bg": "#0A1A40", "surf": "#12265A", "raise": "#1A3170", "bord": "#2A4590", "line": "#1E3878", "line2": "#24407F", "mut": "#A8BBE6", "mut2": "#8499CC",
       "sub": "#D5E0F7", "ink": "#FFF8E7", "acc": "#F7C948", "onacc": "#0A1A40", "bar": "#1E3A8A", "cellb": "#C9D6F2", "cellf": "#EEF3FF", "rgb_bg": "10,26,64", "rgb_acc": "247,201,72", "rgb_ink": "255,248,231"},
}
# light-on-dark text shades that the Day theme has to darken
X = {"#e7ecf6": "#1C1A16", "#c9d3ea": "#3D382F", "#8fa0c4": "#6B6457", "#9aa6c0": "#6B6457", "#c9bfae": "#8A8273", "#ffb4b4": "#B3261E", "#7f8daa": "#6B6457"}
XN = {h: f"x{i}" for i, h in enumerate(X)}
RGBS = (("7,20,43", "rgb_bg"), ("10,24,50", "rgb_bg"), ("6,14,32", "rgb_bg"), ("233,196,107", "rgb_acc"), ("248,244,232", "rgb_ink"))

BLACK = {"bg": "#0A0A0B", "surf": "#151517", "raise": "#1D1D20", "bord": "#2C2C31", "line": "#222226", "line2": "#27272C", "mut": "#A1A1AA", "mut2": "#7C7C85",
         "sub": "#D4D4D8", "ink": "#F5F3EE", "acc": "#E3BC5E", "onacc": "#141006", "bar": "#26262B", "cellb": "#DADAE0", "cellf": "#F4F4F6",
         "rgb_bg": "10,10,11", "rgb_acc": "227,188,94", "rgb_ink": "245,243,238"}
THEMES = {"black": BLACK, "day": T["B"], "starry": T["C"]}
META = {"black": "#0A0A0B", "day": "#F3EFE6", "starry": "#0A1A40"}

def vars_for(k):
    v = THEMES[k]
    out = "".join(f"--r-{r}:{v[r]};" for r in sorted(set(ROLE.values())))
    out += "".join(f"--r-{r}:{v[r]};" for r in ("rgb_bg", "rgb_acc", "rgb_ink"))
    out += "".join(f"--{XN[h]}:{X[h] if k == 'day' else h};" for h in X)
    return out

ATTR = re.compile(r'(?:fill|stroke|stop-color|content|color|flood-color)="$')
def sub_hex(s):
    def rep(m):
        h = m.group(0).lower(); pre = s[max(0, m.start() - 12):m.start()]
        if ATTR.search(pre): return m.group(0)          # SVG / meta attributes can't take var()
        if h in ROLE: return f"var(--r-{ROLE[h]})"
        if h in XN: return f"var(--{XN[h]})"
        return m.group(0)
    return re.sub(r"#[0-9a-fA-F]{6}\b", rep, s)

ICON = {
 "black": '<svg viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="8" fill="#0A0A0B" stroke="currentColor" stroke-width="2"/></svg>',
 "day": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2" fill="currentColor"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3 7 7M17 17l1.7 1.7M5.3 18.7 7 17M17 7l1.7-1.7"/></svg>',
 "starry": '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M15.5 3.5a8.5 8.5 0 1 0 5 13.2A7 7 0 1 1 15.5 3.5z" fill="#F7C948"/><path d="M19 3l.7 1.8 1.8.7-1.8.7L19 8l-.7-1.8-1.8-.7 1.8-.7z" fill="#FFF3C4"/></svg>'}
LABEL = {"black": "Black", "day": "Day", "starry": "Starry Night"}
SWITCH = ('<div class="thsw" role="group" aria-label="Theme">'
          + "".join(f'<button type="button" data-th="{k}" aria-label="{LABEL[k]}" title="{LABEL[k]}">{ICON[k]}</button>' for k in THEMES) + "</div>")

# GA4: the theme rides on every hit as user property ui_theme (queued before gtag("config") so the
# first page_view carries it); a theme_select event fires on each button press.
HEAD_JS = ('<script>try{var t=localStorage.getItem("th");if(!/^(black|day|starry)$/.test(t))t="black"}catch(e){t="black"}'
           'document.documentElement.setAttribute("data-th",t);window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
           'gtag("set","user_properties",{ui_theme:t})</script>')
DAY_FIX = ('[data-th=day] .dbooks button i,[data-th=day] .bksec i{color:#1C1A16!important}[data-th=day] .spd b,[data-th=day] .sch3 .tm{color:#7A5A00}'
           '[data-th=day] .mark [fill="#F8F4E8"]{fill:#1C1A16}[data-th=day] .mark [stroke="#F8F4E8"],[data-th=day] .mark [stroke="#FFF7DE"]{stroke:#1C1A16}[data-th=day] .mark [fill="#E9C46B"],[data-th=day] .mark [fill="#FFF3CF"]{fill:#A87A00}[data-th=day] .mark [stroke="#E9C46B"]{stroke:#A87A00}'
           '[data-th=day] .mtop{color:#1C1A16}[data-th=day] .mtt small{opacity:.85}[data-th=day] .bell{background:#1C1A16}[data-th=day] .chev{background:rgba(28,26,22,.14)}'
           '[data-th=day] .chev::before{border-color:#1C1A16}[data-th=day] .bell::after,[data-th=day] .bell::before{border-color:rgba(28,26,22,.5)}'
           '[data-th=day] .seo a{color:#1F4FB5;text-decoration-color:rgba(31,79,181,.45)}[data-th=day] .seo a:hover{color:#163A8A}[data-th=day] .fl nav b{color:#7A5A00}'
           '[data-th=day] .msum span{background:#1C1A16;color:#FFD34D}[data-th=day] .msum .wn{background:#FFFFFF;color:#1C1A16}[data-th=day] .msum .mlv{background:#c81e1e;color:#fff}'
           '[data-th=day] .mit{background:#FAF7F0;border-color:#E2DACB}[data-th=day] .mit .n,[data-th=day] .mit .st b{color:#1C1A16}[data-th=day] .mit .tg{background:#E8E1D3;color:#3D382F}'
           '[data-th=day] .mit .x{background:rgba(28,26,22,.06)}[data-th=day] .mit.won{background:linear-gradient(90deg,#FFF0B8,#FFF9E6);border-color:#C99A00}'
           '[data-th=day] .mit.won .n,[data-th=day] .mit.won .st b{color:#7A5A00}[data-th=day] .mlive{color:#0F766E}[data-th=day] .mlive.on{color:#B3261E}'
           '[data-th=day] .tk .pz em,[data-th=day] .op[aria-pressed=true],[data-th=day] .hx-tiers div,[data-th=day] .hx-co .hb span,[data-th=day] .hx-it .pz,[data-th=day] .rc>header,[data-th=day] .mtoast{color:#1C1A16}'
           '[data-th=day] .op[aria-pressed=true] i{background:#1C1A16!important}[data-th=day] .hx{background:radial-gradient(120% 120% at 100% 0,#F6E7BF 0,var(--r-surf) 55%)}[data-th=day] .hx-none,[data-th=day] .hx-strip .hy{color:#6B6457}'
           '[data-th=day] .hx-tg button{color:#1C1A16;border-color:#B8AE9C}[data-th=day] .hx-tg button.on{color:#000}'
           '[data-th=day] header,[data-th=day] .nav,[data-th=day] .bnav{color:#1C1A16}[data-th=day] .bar .bt small{color:#6B6457}')
SW_CSS = ('.thsw{display:flex;gap:2px;padding:3px;margin-left:auto;margin-right:8px;border-radius:999px;background:rgba(var(--r-rgb_ink),.08);border:1px solid var(--r-bord)}'
          '.thsw button{display:grid;place-items:center;width:30px;height:30px;border:0;border-radius:999px;background:none;color:var(--r-mut);cursor:pointer;padding:0}'
          '.thsw button[aria-pressed=true]{background:var(--r-acc);color:var(--r-onacc);box-shadow:0 0 0 1px rgba(var(--r-rgb_acc),.5),0 0 12px rgba(var(--r-rgb_acc),.35)}'
          '.thsw button[data-th=starry][aria-pressed=true]{background:#1E3A8A}'
          '@media (max-width:380px){.thsw button{width:27px;height:27px}}')

def starry_css():
    """CSS that ships inside the lazy sky fragment."""
    c = sky.CSS.replace("\n", "")
    c = c.replace("html{background:#050F2A}body{background:transparent}", "[data-th=starry] body{background:transparent}")
    c = c.replace(".slip .lbar,.slip .sec{", "[data-th=starry] .slip .lbar,[data-th=starry] .slip .sec{")
    c = c.replace(".vg-moon{display:none}.vg-hm{display:block}", ".vg-moon{display:none}")
    return c + (".vg::after{content:\"\";position:absolute;z-index:1;top:0;bottom:0;left:50%;width:min(100%,1160px);transform:translateX(-50%);"
                "background:linear-gradient(90deg,transparent,rgba(5,15,42,.84) 44px,rgba(5,15,42,.84) calc(100% - 44px),transparent)}"
                "@media (min-width:760px){.vg-ms{z-index:2}}:root:not([data-th=starry]) .vg{display:none}")

def fragment():
    return "<style>" + starry_css() + "</style>" + sky.LAYER

# iOS 26 Safari ignores theme-color and tints its top/bottom bars from the page: the body
# background or a fixed/sticky bar at the edge. A backdrop-filter on that bar stops the sampling,
# so the two edge bars are
# solid theme colour with no blur. (The date input is color-scheme:dark; Day sets it light.)
INLINE_CSS_TAIL = ("html{background:var(--r-bg)}[data-th=starry]{background:#050F2A}[data-th=day] input{color-scheme:light}"
                   "body>header,.bnav{-webkit-backdrop-filter:none!important;backdrop-filter:none!important;background-color:var(--r-bg)!important}")

def body_js(sky_url):
    return ('<script>(function(){var M=' + str(META).replace("'", '"') + ',r=document.documentElement,m=document.querySelector("meta[name=theme-color]"),k=0;'
            'function sky(){if(k)return;k=1;fetch("' + sky_url + '").then(function(x){return x.ok?x.text():""}).then(function(h){if(h)document.body.insertAdjacentHTML("afterbegin",h)}).catch(function(){k=0})}'
            'function set(t){r.setAttribute("data-th",t);if(m)m.content=M[t];if(t==="starry")sky();document.querySelectorAll(".thsw button").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.th===t)});try{localStorage.setItem("th",t)}catch(e){}}'
            'document.querySelectorAll(".thsw button").forEach(function(b){b.addEventListener("click",function(){var f=r.getAttribute("data-th"),t=b.dataset.th;if(f===t)return;set(t);try{gtag("set","user_properties",{ui_theme:t});gtag("event","theme_select",{theme:t,theme_from:f})}catch(e){}})});'
            'set(r.getAttribute("data-th")||"black")})()</script>')

def write_fragment(out: Path) -> str:
    b = fragment().encode()
    name = f"assets/sky.{hashlib.sha256(b).hexdigest()[:10]}.txt"   # not .html: Pages 308-redirects .html to pretty URLs
    (out / name).parent.mkdir(parents=True, exist_ok=True); (out / name).write_bytes(b)
    return "/" + name

def apply(html: str, sky_url: str) -> str:
    s = sub_hex(html)
    for a, r in RGBS: s = s.replace("rgba(" + a, f"rgba(var(--r-{r})")
    css = (":root,[data-th=black]{" + vars_for("black") + "}[data-th=starry]{" + vars_for("starry") + "}[data-th=day]{" + vars_for("day") + "}"
           + DAY_FIX + SW_CSS + INLINE_CSS_TAIL)
    for a, b, n in (("<head>", "<head>" + HEAD_JS, 1), ("</style>", css + "</style>", 1), ('<div class="lsel">', SWITCH + '<div class="lsel">', 1), ("</body>", body_js(sky_url) + "</body>", 1)):
        assert s.count(a) >= 1, a
        s = s.replace(a, b, n)
    return s
