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


def star4(x, y, r, fill, op=1.0):
    k = r * 0.22
    d = "M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z" % (
        x, y - r, x + k, y - k, x + r, y, x + k, y + k, x, y + r, x - k, y + k, x - r, y, x - k, y - k)
    return '<path d="%s" fill="%s" opacity="%.2f"/>' % (d, fill, op)


def bread(x, y, r, rnd, base="#d9a35f", light="#f3d49a", dark="#a8702f"):
    """a flat piece of bread: shadow, body, lit facet"""
    n = rnd.choice((5, 6, 7))
    a0 = rnd.uniform(0, 6.28)
    P = []
    for i in range(n):
        a = a0 + i * 2 * math.pi / n + rnd.uniform(-0.28, 0.28)
        rr = r * rnd.uniform(0.6, 1.1)
        P.append((rr * math.cos(a), rr * math.sin(a) * 0.85))
    f = lambda pts, dx=0, dy=0, k=1.0: " ".join("%.1f,%.1f" % (x + dx + p[0] * k, y + dy + p[1] * k) for p in pts)
    return ('<polygon points="%s" fill="#06292e" opacity="0.28"/>' % f(P, r * 0.18, r * 0.28) +
            '<polygon points="%s" fill="%s"/>' % (f(P), base) +
            '<polygon points="%s" fill="%s"/>' % (f(P[: max(3, n // 2 + 1)] + [(0, 0)], -r * 0.05, -r * 0.08, 0.95), light) +
            '<polygon points="%s" fill="%s" opacity="0.55"/>' % (f(P[n // 2:] + [P[0], (0, 0)], 0, 0, 0.98), dark))


BEIGE, SAND, TURQ, DEEP, INK = "#eadfc8", "#d9c8a5", "#19a7a1", "#0c5d63", "#062f35"


def blob(x, y, r, rnd, fill, rot=None):
    """a small rounded crumb"""
    n = 7
    a0 = rnd.uniform(0, 6.28) if rot is None else rot
    P = []
    for k in range(n):
        a = a0 + k * 2 * math.pi / n
        rr = r * rnd.uniform(0.78, 1.08)
        P.append((x + rr * math.cos(a), y + rr * math.sin(a) * 0.86))
    d = "M %.1f %.1f " % ((P[0][0] + P[-1][0]) / 2, (P[0][1] + P[-1][1]) / 2)
    for k in range(n):
        q, nx = P[k], P[(k + 1) % n]
        d += "Q %.1f %.1f %.1f %.1f " % (q[0], q[1], (q[0] + nx[0]) / 2, (q[1] + nx[1]) / 2)
    return '<path d="%sZ" fill="%s"/>' % (d, fill)


def spiral(cx, cy, n, spread, rnd, inner, R, big, back=False):
    """crumbs along the golden-angle spiral: bread inside the bowl, stars once they leave it"""
    out = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(1, n):
        r = spread * math.sqrt(i)
        a = i * ga
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if r < R - 12:
            t = r / R
            size = big * (0.25 + 0.75 * t ** 0.9)
            col = "#fff1c9" if t < 0.18 else ("#f6cd7d" if t < 0.55 else "#e0a14e")
            out.append('<g opacity="0.25"><path d="M0 0" /></g>' if False else blob(x + 1.4, y + 2.2, size, rnd, "#06292e"))
            out.append(blob(x, y, size, rnd, col))
        else:
            t = min(1.0, (r - R) / 380)
            sz = (1 - t) ** 1.3 * 9.5 + 1.6
            if (y < 835 or back) and rnd.random() < 0.30 * (1 - 0.6 * t) + 0.04:
                out.append(star4(x, y, sz, inner if rnd.random() < 0.7 else "#c9853f", 0.95 - 0.55 * t))
    return "".join(out)


def flat(u, back=False):
    rnd = random.Random(5)
    b = ["""<defs>
  <radialGradient id="bg{u}" cx="0.5" cy="0.38" r="0.85"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></radialGradient>
  <radialGradient id="bowl{u}" cx="0.5" cy="0.45" r="0.62"><stop offset="0" stop-color="#27bfb7"/><stop offset="0.75" stop-color="#14a09b"/><stop offset="1" stop-color="#0d7f85"/></radialGradient>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0 0.12  0 0 0 0.55 -0.12"/>
  </filter>
</defs>""".format(u=u, c0="#13777b" if back else "#f3ead7", c1="#084a50" if back else "#d9ccb0"),
         '<rect width="%d" height="%d" fill="url(#bg%s)"/>' % (VW, VH, u)]
    if back:
        cx, cy, R = 650, 985, 215
    else:
        cx, cy, R = 340, 628, 200
    b.append('<circle cx="%d" cy="%d" r="%d" fill="#06292e" opacity="0.2"/>' % (cx + 9, cy + 13, R + 14))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, R + 14, SAND if not back else "#0a4c52"))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="url(#bowl%s)"/>' % (cx, cy, R, u))
    b.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="#e9fffb" stroke-width="1" opacity="0.4"/>' % (cx, cy, R - 9))
    star_col = DEEP if not back else "#bfe9e3"
    b.append(spiral(cx, cy, 1700 if not back else 1200, 8.0 if not back else 8.2, rnd, star_col, R, 8.6, back))
    if not back:
        for _ in range(30):
            x, y = rnd.uniform(40, 640), rnd.uniform(30, 330)
            b.append(star4(x, y, rnd.uniform(2.5, 6), DEEP, 0.5))
    b.append('<rect width="%d" height="%d" filter="url(#grain%s)" opacity="0.5" style="mix-blend-mode:multiply"/>' % (VW, VH, u))
    return '<svg class="art" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def main():
    paras = "".join("<p>%s</p>" % plain(t) for t in BACK_TEXT)
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Noto Kufi"; font-weight: 800; src: url(../fonts/noto-kufi-arabic-arabic-800-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 300; src: url(../fonts/cairo-arabic-300-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 400; src: url(../fonts/cairo-arabic-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Cairo"; font-weight: 700; src: url(../fonts/cairo-arabic-700-normal.woff2) format("woff2"); }}
@page {{ size: 170mm 240mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 170mm; height: 240mm; overflow: hidden; break-after: page; background: #eadfc8; }}
.art {{ position: absolute; inset: 0; width: 100%; height: 100%; }}

.title {{
  position: absolute; left: 0; right: 0; top: 15mm; text-align: center;
  font-family: "Noto Kufi", sans-serif; font-weight: 800; line-height: 1.0; color: #062f35;
}}
.title .t1 {{ display: block; font-size: 46pt; color: #0c5d63; }}
.title .t2 {{ display: block; font-size: 88pt; margin-top: 0.5mm; letter-spacing: -0.5pt; }}
.author {{
  position: absolute; left: 0; right: 0; bottom: 13mm; text-align: center; color: #062f35;
  font-family: "Cairo", sans-serif;
}}
.author small {{ display: block; font-weight: 400; font-size: 10.5pt; color: #0c5d63; margin-bottom: 0.5mm; }}
.author b {{ font-weight: 700; font-size: 19pt; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}

.text {{
  position: absolute; left: 22mm; right: 22mm; top: 38mm; height: 118mm;
  display: flex; flex-direction: column; justify-content: center;
}}
.text::before {{ content: ""; display: block; width: 16mm; border-top: 1.6pt solid #e9c98e; margin-bottom: 7mm; }}
.text p {{
  margin: 0 0 3.2mm; text-align: justify;
  font-family: "Cairo", sans-serif; font-weight: 400; font-size: 11.2pt; line-height: 1.95; color: #f4ecd9;
}}
.text p:last-child {{ margin: 0; font-weight: 700; color: #f2cf92; }}
.sign {{ position: absolute; left: 20mm; width: 70mm; top: 205mm; text-align: right; color: #f4ecd9; font-family: "Cairo", sans-serif; }}
.sign .bt {{ display: block; font-family: "Noto Kufi", sans-serif; font-weight: 800; font-size: 23pt; line-height: 1.2; }}
.sign .ba {{ font-weight: 400; font-size: 12pt; color: #f2cf92; font-feature-settings: "rlig" 0, "liga" 0, "calt" 0; }}
</style></head><body>
<div class="page">{front}
  <div class="title"><span class="t1">ثرائد</span><span class="t2">التقوى</span></div>
  <div class="author"><small>تأليف</small><b>محمد عبدالله</b></div>
</div>
<div class="page">{back}<div class="text">{paras}</div>
  <div class="sign"><span class="bt">ثرائد التقوى</span><span class="ba">محمد عبدالله</span></div>
</div>
</body></html>""".format(front=flat("a"), back=flat("b", back=True), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
