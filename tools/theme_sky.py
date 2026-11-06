"""Starry Night theme: the hand-drawn Van Gogh sky (moon curls, curl-halo stars, flowing cloud bands, cypress).

Everything is inline SVG generated here (no image requests). Motion uses only transform/opacity
on whole layers so it stays on the compositor, and it is switched off for reduced-motion users.
"""
import math, random

random.seed(7)
f = lambda v: str(int(round(v)))


def smooth(pts, dp=0):
    """Catmull-Rom through the points, written as cubic Beziers (no visible corners)."""
    g = (lambda v: str(int(round(v)))) if dp == 0 else (lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    d = f"M{g(pts[0][0])},{g(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1, p2 = pts[i], pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{g(c1[0])},{g(c1[1])} {g(c2[0])},{g(c2[1])} {g(p2[0])},{g(p2[1])}"
    return d

def spiral(cx, cy, r0, r1, turns, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n; a = t * turns * 2 * math.pi; r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * 0.62 * math.sin(a)))
    return smooth(pts)

def wave(y0, amp, ph, k1, k2, step=96):
    T = 2 * math.pi / 1440
    pts = [(x, y0 + amp * math.sin(x * T * k1 + ph) + 0.35 * amp * math.sin(x * T * k2 + ph * 2)) for x in range(0, 1441, step)]
    return smooth(pts)

# --- sky field: two looping bands of brush strokes (each tile is exactly 1440 wide and
# repeated once, so translateX(-50%) loops with no seam) + the big double swirl ------------
cols = ["#2E57C9", "#4A78E0", "#7FA6F0", "#A9C6F7", "#F7C948"]
BAND = {0: [], 1: []}
for i, y in enumerate(range(60, 620, 40)):
    c = cols[i % 4] if i % 5 else cols[4]
    op = .18 if c != "#F7C948" else .13
    BAND[i % 2].append(f'<path d="{wave(y, 18 + (i % 3) * 9, i * .9, 2 + i % 2, 5 + i % 3)}" stroke="{c}" stroke-opacity="{op}" stroke-width="{3 + i % 3}" stroke-dasharray="{16 + i % 3 * 6} {10 + i % 4 * 3}"/>')
for r0, c in ((8, "#F7C948"), (24, "#A9C6F7")):
    BAND[0].append(f'<path d="{spiral(1010, 330, r0, r0 + 70, 1.3, 14)}" stroke="{c}" stroke-opacity=".28" stroke-width="3" stroke-dasharray="12 8"/>')
def band(n):
    return (f'<svg class="vg-band vg-b{n}" viewBox="0 0 2880 700" preserveAspectRatio="xMinYMin meet" fill="none" stroke-linecap="round">'
            f'<g id="vgb{n}">' + "".join(BAND[n]) + f'</g><use href="#vgb{n}" x="1440"/></svg>')
SW = "".join(f'<path d="{spiral(700, 230, r0, r0 + 150, 1.6, 22)}" stroke="{c}" stroke-opacity=".34" stroke-width="{w}" stroke-dasharray="18 9"/>'
             for r0, c, w in ((12, "#A9C6F7", 5), (30, "#F7C948", 3), (55, "#4A78E0", 4), (80, "#7FA6F0", 3)))
FIELD = band(0) + band(1) + f'<svg class="vg-swirl" viewBox="440 70 520 320" fill="none" stroke-linecap="round">{SW}</svg>'

# --- stars ---------------------------------------------------------------------------------
# small twinklers: plain spans (opacity-only animation, composited)
SMALL = [(4, 22), (13, 6), (24, 30), (35, 15), (44, 4), (53, 33), (59, 18), (70, 8), (77, 30), (96, 24), (8, 48), (27, 56), (67, 44), (90, 60), (16, 84), (83, 90), (45, 62), (98, 40)]
SMALLS = "".join(f'<i class="vg-s" style="left:{x}%;top:{y}%;animation-delay:-{(k * 0.73) % 4:.1f}s"></i>' for k, (x, y) in enumerate(SMALL))

def curl_star(n):
    """Van Gogh star: bright core, glow ring and two spiral arms of dashed brushstrokes."""
    arms = ""
    for a0, c, w in ((0, "#FFE7A3", 3), (math.pi, "#F7C948", 2.6), (math.pi / 2, "#A9C6F7", 2)):
        pts = []
        for k in range(14):
            t = k / 13; a = a0 + t * 2.4 * math.pi; r = 14 + 34 * t
            pts.append((50 + r * math.cos(a), 50 + r * math.sin(a)))
        arms += f'<path d="{smooth(pts, 1)}" stroke="{c}" stroke-opacity=".6" stroke-width="{w}" stroke-dasharray="9 6" stroke-linecap="round" fill="none"/>'
    return (f'<svg width="0" height="0"><symbol id="vgcs" viewBox="0 0 100 100">{arms}'
            '<circle cx="50" cy="50" r="13" fill="#F7C948" fill-opacity=".18"/><circle cx="50" cy="50" r="7" fill="#FFF3C4"/></symbol></svg>')
BIG = [(7, 12, 1.0, 1), (29, 22, .75, -1), (55, 10, .85, 1), (19, 46, .7, -1), (91, 44, .9, 1), (63, 36, .6, -1), (6, 68, .8, 1), (94, 74, .7, -1)]
CURL = curl_star(0)
BIGS = CURL + "".join(f'<span class="vg-big{" rev" if d < 0 else ""}" style="left:{x}%;top:{y}%;--s:{sc};animation-delay:-{k * 1.3:.1f}s"><svg viewBox="0 0 100 100"><use href="#vgcs"/></svg></span>'
               for k, (x, y, sc, d) in enumerate(BIG))
STARSVG = SMALLS + BIGS

# --- moon scene: cloud lines sweep in from the left, over the top and curl into the moon ------
MX, MY = 470, 150
def into_moon(r0, a0, turns, sq, r_end, n=16):
    pts = []
    for k in range(n + 1):
        t = k / n; e = 1 - (1 - t) ** 2              # ease: long sweep, tight finish
        a = a0 + e * turns * 2 * math.pi; r = r0 + (r_end - r0) * e
        pts.append((MX + r * math.cos(a), MY + r * sq * math.sin(a)))
    return smooth(pts)
CL = ""
for r0, a0, c, w, sq, r_end in ((480, math.pi * .98, "#7FA6F0", 6, .52, 132), (440, math.pi * 1.03, "#F7C948", 4, .5, 112),
                                (405, math.pi * .94, "#A9C6F7", 5, .6, 124), (365, math.pi * 1.07, "#4A78E0", 6, .46, 104)):
    d = into_moon(r0, a0, .92, sq, r_end)
    CL += (f'<path d="{d}" stroke="{c}" stroke-opacity=".16" stroke-width="{w * 2.6:.0f}" stroke-linecap="round"/>'
           f'<path d="{d}" stroke="{c}" stroke-opacity=".55" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="70 16 30 12"/>')
def _moon():
    # crescent = disc minus an offset disc (mask), painted with concentric dashed brush arcs
    strokes = ""
    pal = ("#FFF3C4", "#FFE07A", "#F7C948", "#F5A524", "#FFE9A8", "#E8952A")
    for k, r in enumerate(range(10, 52, 4)):
        c = pal[k % len(pal)]; dash = (7 + k % 3 * 2, 3 + k % 2 * 2)
        strokes += (f'<circle cx="{MX}" cy="{MY}" r="{r}" stroke="{c}" stroke-width="{4.2 - k * .12:.1f}" stroke-dasharray="{dash[0]} {dash[1]}" '
                    f'stroke-dashoffset="{k * 5}" stroke-linecap="round"/>')
    disc = (f'<defs><mask id="vgmm"><circle cx="{MX}" cy="{MY}" r="52" fill="#fff"/><circle cx="{MX + 24}" cy="{MY - 15}" r="43" fill="#000"/></mask>'
            '<radialGradient id="vgmg"><stop offset=".44" stop-color="#F7C948" stop-opacity="0"/><stop offset=".5" stop-color="#F7C948" stop-opacity=".26"/><stop offset=".7" stop-color="#E8952A" stop-opacity=".1"/>'
            '<stop offset="1" stop-color="#E8952A" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{MX}" cy="{MY}" r="112" fill="url(#vgmg)"/>'
            f'<g mask="url(#vgmm)"><circle cx="{MX}" cy="{MY}" r="52" fill="#E9B23A"/>{strokes}</g>')
    # halo: rings of short brush dashes in yellows and oranges (rotates slowly as its own layer)
    halo = ""
    for k, (r, c, w, d, o) in enumerate(((60, "#FFE07A", 4, "9 7", .55), (68, "#F5A524", 3.5, "6 6", .45), (76, "#FFF3C4", 3, "12 8", .4),
                                         (84, "#F7C948", 4, "7 9", .35), (93, "#E8952A", 3, "10 10", .28), (102, "#FFE9A8", 2.5, "5 9", .22))):
        halo += f'<circle cx="{MX}" cy="{MY}" r="{r}" stroke="{c}" stroke-opacity="{o}" stroke-width="{w}" stroke-dasharray="{d}" stroke-dashoffset="{k * 7}" stroke-linecap="round"/>'
    return (f'<svg class="vg-mh" viewBox="0 0 600 400" fill="none">{halo}</svg>'
            f'<svg class="vg-mo" viewBox="0 0 600 400" fill="none">{disc}</svg>')
MOON = ('<div class="vg-ms">'
        f'<svg class="vg-mc" viewBox="0 0 600 400" fill="none">{CL}</svg>' + _moon() + '</div>')

# --- cypress flame + village hills ---------------------------------------------------------
cyp = []
for i in range(7):
    w = 34 - i * 4
    cyp.append(f'<path d="M{60-w},400 C{55-w},{300-i*20} {80-w/2},{180-i*15} {72+i*2},{20+i*10} C{90+w/3},{150-i*12} {108+w/2},{280-i*18} {86+w},400" '
               f'fill="none" stroke="{["#0E2A44","#163A5C","#1F4E73","#0B2238"][i%4]}" stroke-width="{7-i*.6:.1f}" stroke-dasharray="20 7"/>')
CYPRESS = ('<svg class="vg-cyp" viewBox="0 0 150 400" preserveAspectRatio="xMinYMax meet">'
           '<path d="M40,400 C30,300 50,170 72,20 C95,170 118,300 108,400Z" fill="#06142A"/>' + "".join(cyp) + "</svg>")
HILLS = ('<svg class="vg-hills" viewBox="0 0 1440 160" preserveAspectRatio="none">'
         '<path d="M0,90 C200,40 380,110 620,70 C860,30 1100,100 1440,60 V160 H0Z" fill="#0A1838"/>'
         '<path d="M0,120 C260,90 520,140 800,110 C1060,85 1260,130 1440,105 V160 H0Z" fill="#071230"/>'
         + "".join(f'<rect x="{x}" y="{y}" width="5" height="5" fill="#F7C948" opacity=".75"/>' for x, y in ((280, 122), (318, 118), (520, 128), (905, 112), (948, 116), (1180, 114)))
         + '<path d="M300,118 l12,-12 l12,12M930,108 l14,-14 l14,14" stroke="#0A1838" stroke-width="6" fill="none"/></svg>')

LAYER = f'<div class="vg" aria-hidden="true">{FIELD}{STARSVG}{MOON}{CYPRESS}</div>'

# brushwork texture for the royal-blue prize bars (one tiny tiled SVG)
BRUSH = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='24'%3E%3Cpath d='M-5 8c20-6 40 6 65 0s45-6 70 0M-5 18c22-5 42 5 64 0s46-5 70 0' "
         "fill='none' stroke='%237FA6F0' stroke-opacity='.18' stroke-width='2.2' stroke-dasharray='10 6' stroke-linecap='round'/%3E%3C/svg%3E")

CSS = f"""
html{{background:#050F2A}}body{{background:transparent}}
.vg{{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;background:radial-gradient(120% 70% at 50% 0,#0E2560 0,#071535 55%,#030A1F 100%)}}
.vg svg{{position:absolute}}.vg-hm{{display:none;position:absolute;top:50%;right:92px;width:46px;height:46px;margin-top:-23px;pointer-events:none}}
.vg-band{{top:0;left:0;height:78vh;width:calc(78vh*2880/700);will-change:transform;animation:vgflow 80s linear infinite}}.vg-b1{{animation-duration:130s;top:2vh}}.vg-swirl{{left:50%;top:7.8vh;height:calc(78vh*320/700);width:calc(78vh*520/700);margin-left:calc(78vh*-260/700);will-change:transform;animation:vgspin 18s ease-in-out infinite alternate}}

.vg-ms{{position:absolute;top:52px;right:-1vw;width:clamp(320px,44vw,660px);aspect-ratio:3/2}}.vg-ms svg{{inset:0;width:100%;height:100%}}.vg-mc{{transform-origin:78.3% 37.5%;will-change:transform;animation:vgcurl 16s ease-in-out infinite alternate}}.vg-mh{{transform-origin:78.3% 37.5%;will-change:transform;animation:vgspin2 90s linear infinite}}.vg-s{{position:absolute;width:3px;height:3px;border-radius:50%;background:#FFF3C4;box-shadow:0 0 6px 2px rgba(247,201,72,.55);animation:vgtw 4.2s ease-in-out infinite}}.vg-big{{position:absolute;width:calc(clamp(64px,8vw,120px)*var(--s));aspect-ratio:1;margin:calc(clamp(64px,8vw,120px)*var(--s)/-2) 0 0 calc(clamp(64px,8vw,120px)*var(--s)/-2);animation:vgpulse 6s ease-in-out infinite}}.vg-big svg{{position:absolute;inset:0;width:100%;height:100%;will-change:transform;animation:vgspin2 38s linear infinite}}.vg-big.rev svg{{animation-direction:reverse;animation-duration:52s}}
.vg-hills{{left:0;right:0;bottom:0;width:100%;height:clamp(70px,13vh,150px)}}
.vg-cyp{{left:max(-14px,1vw);bottom:0;height:clamp(200px,52vh,520px);width:auto;transform-origin:50% 100%;animation:vgsway 7s cubic-bezier(.45,.05,.55,.95) infinite alternate}}

@keyframes vgflow{{to{{transform:translate3d(-50%,0,0)}}}}@keyframes vgspin{{from{{transform:rotate(-5deg) scale(.97)}}to{{transform:rotate(6deg) scale(1.03)}}}}
@keyframes vgsway{{from{{transform:skewX(1.8deg) rotate(-.6deg)}}to{{transform:skewX(-2.4deg) rotate(.8deg)}}}}
@keyframes vgtw{{50%{{opacity:.25}}}}@keyframes vgpulse{{50%{{transform:scale(1.08);opacity:.85}}}}@keyframes vgspin2{{to{{transform:rotate(360deg)}}}}@keyframes vgcurl{{from{{transform:rotate(-7deg)}}to{{transform:rotate(5deg)}}}}
@media (prefers-reduced-motion:reduce){{.vg *{{animation:none!important}}}}
@media (max-width:640px){{.vg-band,.vg-swirl{{opacity:.75}}.vg-cyp{{height:34vh}}.vg-ms{{top:80px;right:-12px;width:230px}}.vg-mc{{opacity:.85}}}}
.slip .lbar,.slip .sec{{background-image:url("{BRUSH}");background-size:120px 24px}}
"""
