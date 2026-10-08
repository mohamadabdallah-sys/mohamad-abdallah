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


def sky_and_sun(u, dark=False):
    top, mid, hor = ("#1a2433", "#4a3a4a", "#c98a5e") if dark else ("#3a4d63", "#a98a86", "#f0c487")
    return """<defs>
  <linearGradient id="sky{u}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{top}"/><stop offset="0.38" stop-color="{mid}"/><stop offset="0.66" stop-color="{hor}"/><stop offset="0.8" stop-color="#f6dcab"/>
  </linearGradient>
  <radialGradient id="sun{u}" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff6df"/><stop offset="0.55" stop-color="#fbe2b0"/><stop offset="1" stop-color="#f2b877"/>
  </radialGradient>
  <radialGradient id="halo{u}" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ffe9bd" stop-opacity="0.85"/><stop offset="0.5" stop-color="#f6c98a" stop-opacity="0.28"/><stop offset="1" stop-color="#f6c98a" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="d1{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c98962"/><stop offset="1" stop-color="#8f5a4c"/></linearGradient>
  <linearGradient id="d2{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e5a4e"/><stop offset="1" stop-color="#5b3a41"/></linearGradient>
  <linearGradient id="d3{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f3340"/><stop offset="1" stop-color="#2a1b29"/></linearGradient>
  <linearGradient id="d4{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1b29"/><stop offset="1" stop-color="#150e18"/></linearGradient>
  <filter id="soft{u}" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="soft2{u}" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
  <filter id="grain{u}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.93  0 0 0 0 0.82  0 0 0 0.55 -0.12"/>
  </filter>
</defs>""".format(u=u, top=top, mid=mid, hor=hor)


def haze(u):
    """soft dusty cloud bands"""
    b = ['<g filter="url(#soft{u})" fill="#f8e4c4">'.format(u=u)]
    for cx, cy, rx, ry, op in ((110, 330, 150, 18, .28), (560, 270, 170, 16, .22), (300, 440, 240, 20, .30), (620, 520, 150, 14, .30), (60, 560, 140, 14, .35)):
        b.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" opacity="%.2f"/>' % (cx, cy, rx, ry, op))
    b.append("</g>")
    return "".join(b)


def scene(u, back=False):
    b = [sky_and_sun(u, dark=back),
         '<rect width="%d" height="%d" fill="url(#sky%s)"/>' % (VW, VH, u)]
    cx, cy, r = (420, 700, 120) if back else (420, 590, 150)
    b.append('<circle cx="%d" cy="%d" r="%d" fill="url(#halo%s)"/>' % (cx, cy, r * 3.1, u))
    b.append('<circle cx="%d" cy="%d" r="%d" fill="url(#sun%s)" %s/>' % (cx, cy, r, u, 'opacity="0.78"' if back else ""))
    b.append(haze(u))
    # dunes, far to near
    p1, (x1, y1) = ridge(640, 26, 3, shift=0.3)
    b.append('<path d="%s" fill="url(#d1%s)"/>' % (p1, u))
    b.append('<path d="%s" fill="#ffd9a0" opacity="0.18" filter="url(#soft2%s)"/>' % (ridge(636, 26, 3, shift=0.3)[0], u))
    p2, (x2, y2) = ridge(712, 34, 11, n=7, shift=1.1)
    b.append('<path d="%s" fill="url(#d2%s)"/>' % (p2, u))
    p3, (x3, y3) = ridge(790, 40, 5, n=6, shift=2.0)
    b.append('<path d="%s" fill="url(#d3%s)"/>' % (p3, u))
    p4, (x4, y4) = ridge(880, 30, 9, n=5, shift=0.7)
    b.append('<path d="%s" fill="url(#d4%s)"/>' % (p4, u))
    # sun-lit crest lines
    for (xs, ys), col in (((x2, y2), "#ffd9a0"), ((x3, y3), "#e9a77a")):
        d = "M %.1f %.1f " % (xs[0], ys[0] + 2)
        for i in range(1, len(xs)):
            c = (xs[i - 1] + xs[i]) / 2
            d += "C %.1f %.1f %.1f %.1f %.1f %.1f " % (c, ys[i - 1] + 2, c, ys[i] + 2, xs[i], ys[i] + 2)
        b.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" opacity="0.5"/>' % (d, col))
    if not back:
        # the traveller, on the second dune, with a long shadow and a trail of footprints
        tx, ty = 214, 716
        b.append('<path d="M %d %d L %d %d L %d %d Z" fill="#3b2634" opacity="0.5"/>' % (tx - 6, ty + 5, tx + 210, ty + 30, tx + 14, ty + 10))
        b.append(traveller(tx, ty, 1.85))
        rnd = random.Random(2)
        for i in range(11):
            fx = tx + 44 + i * 26 + rnd.uniform(-2, 2)
            fy = ty + 9 + i * 5.2 + (i * i) * 0.14
            b.append('<ellipse cx="%.1f" cy="%.1f" rx="4.4" ry="1.6" fill="#3b2634" opacity="%.2f"/>' % (fx, fy, 0.5 - i * 0.03))
    # film grain over everything
    b.append('<rect width="%d" height="%d" filter="url(#grain%s)" opacity="0.5" style="mix-blend-mode:soft-light"/>' % (VW, VH, u))
    # top and bottom darkening so the type stays legible
    b.append('<defs><linearGradient id="vt%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101827" stop-opacity="0.85"/><stop offset="0.6" stop-color="#101827" stop-opacity="0.45"/><stop offset="1" stop-color="#101827" stop-opacity="0"/></linearGradient>'
             '<linearGradient id="vb%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0710" stop-opacity="0"/><stop offset="1" stop-color="#0b0710" stop-opacity="0.7"/></linearGradient></defs>' % (u, u))
    b.append('<rect width="%d" height="%d" fill="url(#vt%s)"%s/>' % (VW, 600 if back else 360, u, ' opacity="1"' if back else ""))
    b.append('<rect y="740" width="%d" height="220" fill="url(#vb%s)"/>' % (VW, u))
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
</body></html>""".format(front=scene("a"), back=scene("b", back=True), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
