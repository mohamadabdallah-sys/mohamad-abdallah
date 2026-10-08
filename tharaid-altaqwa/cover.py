# -*- coding: utf-8 -*-
"""Front and back cover (build/cover.html, two 170×240 mm pages): a conceptual illustrated cover —
a traveller with his provision crossing dunes at dusk towards a great pale disc, hazy warm light,
a heavy display title at the top and the author at the foot."""
import os, re, math, random

HERE = os.path.dirname(os.path.abspath(__file__))

BACK_TEXT = [
    "أنا حُلمُ النِّيامِ، وخديعةُ الأيامِ، مَنِ استغنى فيَّ فُتِن، ومَنِ افتقرَ إليَّ حَزِن. "
    "فاحذرني؛ فإنَّ بقاءَك فيَّ كفَيْءِ السحابِ أو وَميضِ السَّراب. "
    "لو كنتُ وفيَّةً لَما خلَّفتُ مَقعدَ حبيبِ ربِّ العالمين، النبيِّ الأكرمِ؛ "
    "ولو كنتُ نافعةً لَما نصبتُ الشِّراكَ للغافلين. "
    "أنا التي طويتُ القرونَ في جَوفي، وأذقتُ الجبابرةَ كأساً من خَوْفي، "
    "لا رَضِيعي سَلِم، ولا مُعمَّري غَنِم.",
    "فيا مَن مَلَّكهُ الأملُ وطولُ المُهلة: بادِرِ العملَ قبل خُفوتِ القبسِ وحلولِ الوَهلة؛ "
    "فما الأيامُ إلا مَراحلُ تُطوى إلى القُبور، وما الفوزُ إلا لمَن خَافَ العُبور، "
    "يومَ يَنكشفُ المستورُ، ويُحصَّلُ ما في الصُّدور.",
]

VW, VH = 680, 960            # 4 units per mm


def plain(s):
    """no tashkeel anywhere on the cover"""
    return re.sub("[\u064B-\u0652\u0670]", "", s)


def ridge(y0, amp, seed, n=9, bottom=VH + 10, shift=0.0):
    """a wind-swept dune line as a closed path (smooth cubic curve through random crests)"""
    rnd = random.Random(seed)
    xs = [-20 + i * (VW + 40) / n for i in range(n + 1)]
    ys = [y0 + amp * math.sin(i * 1.3 + shift) * 0.6 + rnd.uniform(-amp, amp) * 0.5 for i in range(n + 1)]
    d = "M %.1f %.1f " % (xs[0], ys[0])
    for i in range(1, n + 1):
        cx = (xs[i - 1] + xs[i]) / 2
        d += "C %.1f %.1f %.1f %.1f %.1f %.1f " % (cx, ys[i - 1], cx, ys[i], xs[i], ys[i])
    return d + "L %.1f %.1f L %.1f %.1f Z" % (xs[-1], bottom, xs[0], bottom), (xs, ys)


def traveller(x, y, s=1.0, col="#1a1218"):
    """a small cloaked figure with a staff and a bundle on the back, seen from the side (facing left)"""
    g = '<g transform="translate(%.1f %.1f) scale(%.2f)" fill="%s">' % (x, y, s, col)
    g += '<path d="M0 0 C-3 -10 -4 -22 -2 -34 C-1 -40 3 -44 7 -43 C11 -42 12 -37 11 -33 C14 -24 14 -10 15 0 Z"/>'      # cloak
    g += '<circle cx="5" cy="-50" r="6.3"/>'                                                                          # head
    g += '<path d="M-1 -41 C-9 -42 -14 -35 -12 -27 C-8 -26 -4 -29 0 -33 Z"/>'                                       # bundle
    g += '<rect x="-18" y="-60" width="2.4" height="62" rx="1.2" transform="rotate(7 -17 -30)"/>'                    # staff
    g += '<path d="M2 0 L-4 0 L-7 4 L6 4 Z"/>'
    return g + "</g>"


def catmull(pts, n=200):
    """a smooth curve through the given points (Catmull-Rom), as n samples"""
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    segs = len(pts) - 1
    for k in range(segs):
        p0, p1, p2, p3 = P[k], P[k + 1], P[k + 2], P[k + 3]
        for t in [i / (n // segs) for i in range(n // segs)]:
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out.append(pts[-1])
    return out


def crumb(cx, cy, r, rnd, fill):
    """one irregular piece of bread"""
    n = rnd.choice((5, 6, 7))
    a0 = rnd.uniform(0, 6.28)
    pts = []
    for i in range(n):
        a = a0 + i * 2 * math.pi / n + rnd.uniform(-0.25, 0.25)
        rr = r * rnd.uniform(0.62, 1.12)
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.82))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


# the path of crumbs: from the foreground, over the dunes, up into the Milky Way
TRAIL = [(70, 950), (190, 842), (330, 790), (470, 742), (520, 668), (430, 612), (330, 560), (350, 482),
         (450, 420), (520, 340), (570, 250), (600, 150)]


def night(u, back=False):
    rnd = random.Random(11)
    b = ["""<defs>
  <linearGradient id="sky{u}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#050a1c"/><stop offset="0.45" stop-color="#0d1b3a"/><stop offset="0.72" stop-color="#1d3a5c"/><stop offset="0.86" stop-color="#7a6a73"/><stop offset="1" stop-color="#c79a74"/>
  </linearGradient>
  <linearGradient id="gold{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0c4"/><stop offset="0.55" stop-color="#f1b85a"/><stop offset="1" stop-color="#c9822f"/></linearGradient>
  <linearGradient id="dn1{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27415f"/><stop offset="1" stop-color="#101d33"/></linearGradient>
  <linearGradient id="dn2{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16263f"/><stop offset="1" stop-color="#0a1222"/></linearGradient>
  <linearGradient id="dn3{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1526"/><stop offset="1" stop-color="#05080f"/></linearGradient>
  <filter id="glow{u}" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="bigblur{u}" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1100" height="1400"><feGaussianBlur stdDeviation="22"/></filter>
  <filter id="midblur{u}" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1100" height="1400"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.95  0 0 0 0 0.85  0 0 0 0.5 -0.1"/>
  </filter>
</defs>""".format(u=u),
         '<rect width="%d" height="%d" fill="url(#sky%s)"/>' % (VW, VH, u)]
    pts = catmull(TRAIL, 240)
    # the Milky Way: the far end of the trail, widened and blurred
    far = [p for p in pts if p[1] < 640]
    path = "M " + " L ".join("%.1f %.1f" % p for p in far)
    b.append('<path d="%s" fill="none" stroke="#9fb7e8" stroke-opacity="0.20" stroke-width="150" stroke-linecap="round" filter="url(#bigblur%s)"/>' % (path, u))
    b.append('<path d="%s" fill="none" stroke="#f6d9a0" stroke-opacity="0.30" stroke-width="46" stroke-linecap="round" filter="url(#midblur%s)"/>' % (path, u))
    # stars
    for _ in range(260):
        x, y = rnd.uniform(0, VW), rnd.uniform(0, 640)
        r = rnd.choice((0.5, 0.6, 0.8, 1.0, 1.3))
        b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff6e2" opacity="%.2f"/>' % (x, y, r, rnd.uniform(0.25, 0.9)))
    for _ in range(14):
        x, y = rnd.uniform(20, VW - 20), rnd.uniform(20, 560)
        b.append('<circle cx="%.1f" cy="%.1f" r="1.7" fill="#fffbe9" filter="url(#glow%s)"/>' % (x, y, u))
    # warm horizon glow
    b.append('<ellipse cx="300" cy="650" rx="420" ry="90" fill="#f0b97a" opacity="0.34" filter="url(#bigblur%s)"/>' % u)
    # dunes
    d1, (x1, y1) = ridge(640, 24, 21, shift=0.2)
    d2, (x2, y2) = ridge(730, 34, 8, n=7, shift=1.0)
    d3, (x3, y3) = ridge(830, 36, 3, n=6, shift=2.1)
    b.append('<path d="%s" fill="url(#dn1%s)"/>' % (d1, u))
    b.append('<path d="%s" fill="url(#dn2%s)"/>' % (d2, u))
    b.append('<path d="%s" fill="url(#dn3%s)"/>' % (d3, u))
    for (xs, ys), col, op in (((x1, y1), "#f2c28a", .55), ((x2, y2), "#9fb5d6", .28)):
        d = "M %.1f %.1f " % (xs[0], ys[0] + 1.5)
        for i in range(1, len(xs)):
            c = (xs[i - 1] + xs[i]) / 2
            d += "C %.1f %.1f %.1f %.1f %.1f %.1f " % (c, ys[i - 1] + 1.5, c, ys[i] + 1.5, xs[i], ys[i] + 1.5)
        b.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.3" opacity="%.2f"/>' % (d, col, op))
    # the crumbs
    if back:
        sel = [(p, k) for k, p in enumerate(pts)][::5]
        sel = [(p, k) for p, k in sel if 600 < p[1] < 770]
        total = len(pts)
    else:
        sel = [(p, k) for k, p in enumerate(pts)][::3]
        total = len(pts)
    for (x, y), k in sel:
        t = k / total
        size = 17 * (1 - t) ** 1.7 + 2.4
        x += rnd.uniform(-9, 9) * (1 - t) ** 1.2
        y += rnd.uniform(-6, 6) * (1 - t) ** 1.2
        b.append('<g filter="url(#glow%s)">%s</g>' % (u, crumb(x, y, size, rnd, "url(#gold%s)" % u)))
    if not back:
        # a few crumbs drifting up out of the trail like sparks
        for _ in range(26):
            k = rnd.randint(70, 200)
            x, y = pts[k]
            x += rnd.uniform(-45, 45); y += rnd.uniform(-60, 20)
            b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffe3a6" opacity="%.2f" filter="url(#glow%s)"/>' % (x, y, rnd.uniform(0.8, 1.9), rnd.uniform(0.5, 0.95), u))
        # the traveller at the start of the trail
        b.append('<g stroke="#8fa6c8" stroke-width="0.9" stroke-opacity="0.55">%s</g>' % traveller(104, 898, 1.5, col="#070b16"))
    b.append('<rect width="%d" height="%d" filter="url(#grain%s)" opacity="0.45" style="mix-blend-mode:soft-light"/>' % (VW, VH, u))
    b.append('<defs><linearGradient id="vb%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03060d" stop-opacity="0"/><stop offset="1" stop-color="#03060d" stop-opacity="0.75"/></linearGradient></defs>' % u)
    b.append('<rect y="780" width="%d" height="180" fill="url(#vb%s)"/>' % (VW, u))
    return '<svg class="art" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def main():
    paras = "".join("<p>%s</p>" % plain(t) for t in BACK_TEXT)
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Lalezar"; src: url(../fonts/lalezar-arabic-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 300; src: url(../fonts/cairo-arabic-300-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 400; src: url(../fonts/cairo-arabic-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 700; src: url(../fonts/cairo-arabic-700-normal.woff2) format("woff2"); }}
@page {{ size: 170mm 240mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 170mm; height: 240mm; overflow: hidden; break-after: page; background: #1a2433; }}
.art {{ position: absolute; inset: 0; width: 100%; height: 100%; }}

.title {{
  position: absolute; left: 0; right: 0; top: 17mm; text-align: center;
  font-family: "Lalezar", sans-serif; line-height: 0.95; color: #fff3de;
  text-shadow: 0 0.6mm 0 #b5683c, 0 1.2mm 0 #8a4a30, 0 2.4mm 4mm rgba(20,10,10,.45);
}}
.title .t1 {{ display: block; font-size: 62pt; }}
.title .t2 {{ display: block; font-size: 92pt; margin-top: 1mm; }}
.rule {{ position: absolute; left: 50%; top: 100mm; width: 30mm; margin-left: -15mm; border-top: 0.9pt solid rgba(255,236,205,.8); }}
.author {{
  position: absolute; left: 0; right: 0; bottom: 14mm; text-align: center; color: #fbe8cb;
  font-family: "Cairo", sans-serif;
}}
.author small {{ display: block; font-weight: 400; font-size: 11pt; letter-spacing: 0; opacity: 1; color: #f2c88f; margin-bottom: 1mm; }}
.author b {{ font-weight: 700; font-size: 20pt; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}

.text {{
  position: absolute; left: 22mm; right: 22mm; top: 40mm; height: 118mm;
  display: flex; flex-direction: column; justify-content: center;
  padding: 0; box-sizing: border-box;
}}
.text::before {{ content: ""; display: block; width: 16mm; border-top: 1.4pt solid #e9b779; margin-bottom: 7mm; }}
.text p {{
  margin: 0 0 3.2mm; text-align: justify;
  font-family: "Cairo", sans-serif; font-weight: 300; font-size: 11pt; line-height: 1.95; color: #fbf1e0;
}}
.text p:last-child {{ margin: 0; font-weight: 400; color: #f6cf94; }}
.sign {{ position: absolute; left: 0; right: 0; bottom: 14mm; text-align: center; color: #fbe8cb; font-family: "Cairo", sans-serif; }}
.sign .bt {{ display: block; font-family: "Lalezar", sans-serif; font-size: 30pt; line-height: 1.1; text-shadow: 0 0.5mm 0 #b5683c; }}
.sign .ba {{ font-weight: 400; font-size: 12pt; opacity: .9; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}
</style></head><body>
<div class="page">{front}
  <div class="title"><span class="t1">ثرائد</span><span class="t2">التقوى</span></div>
  <div class="author"><small>تأليف</small><b>محمد عبدالله</b></div>
</div>
<div class="page">{back}<div class="text">{paras}</div>
  <div class="sign"><span class="bt">ثرائد التقوى</span><span class="ba">محمد عبدالله</span></div>
</div>
</body></html>""".format(front=night("a"), back=night("b", back=True), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
