# -*- coding: utf-8 -*-
"""Front and back cover (build/cover.html, two 170×240 mm pages), in the style of classical bindings:
a central lobed medallion (shamsa) with pendants, quarter medallions in the corners, an ornamental border band."""
import math, os, re
import ornaments as O

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
G1, G2, G3 = "#f7e6ad", "#c99a45", "#f0d488"
GOLD = "#d8b468"
GROUND = "#0a3428"


def pts(points):
    return " ".join("%.1f,%.1f" % p for p in points)


def lobed(cx, cy, rx, ry, lobes, depth, n=720):
    """an ellipse with a scalloped edge"""
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 - depth * (1 - abs(math.cos(lobes * t / 2))) ** 1.6
        out.append((cx + rx * k * math.sin(t), cy - ry * k * math.cos(t)))
    return out


def rosette(cx, cy, R, color, sw=1.2, op=1.0):
    """layered sixteen-pointed rosette"""
    b = ['<g opacity="%g" fill="none" stroke="%s" stroke-width="%g">' % (op, color, sw)]
    b.append('<polygon points="%s"/>' % O.star(cx, cy, R, R * 0.72, 16))
    b.append('<polygon points="%s"/>' % O.star(cx, cy, R * 0.72, R * 0.5, 8, math.pi / 8))
    b.append('<polygon points="%s"/>' % O.star(cx, cy, R * 0.72, R * 0.5, 8))
    b.append('<circle cx="%g" cy="%g" r="%g"/>' % (cx, cy, R * 0.34))
    b.append('<circle cx="%g" cy="%g" r="%g"/>' % (cx, cy, R * 0.18))
    for i in range(16):
        a = 2 * math.pi * i / 16
        b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (
            cx + R * 0.34 * math.cos(a), cy + R * 0.34 * math.sin(a), cx + R * 0.5 * math.cos(a), cy + R * 0.5 * math.sin(a)))
    b.append("</g>")
    return "".join(b)


def tile(s=68):
    """girih-like background tile: star, octagon ring and joining stars"""
    c = s / 2
    b = [O.khatam(c, c, s * 0.3, GOLD, "none", 0.7)]
    b.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="0.6"/>' % (O.star(c, c, s * 0.5, s * 0.4, 8, math.pi / 8), GOLD))
    for x, y in ((0, 0), (s, 0), (0, s), (s, s)):
        b.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="0.6"/>' % (O.star(x, y, s * 0.2, s * 0.12, 8), GOLD))
    return '<g opacity="0.13">%s</g>' % "".join(b)


def border_band(x0, y0, x1, y1, w):
    """frame: outer and inner gold rules with a chain of small stars between them"""
    b = []
    for off, sw in ((0, 2.6), (5, 0.8), (w - 5, 0.8), (w, 2.6)):
        b.append('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s" stroke-width="%g"/>'
                 % (x0 + off, y0 + off, x1 - x0 - 2 * off, y1 - y0 - 2 * off, GOLD, sw))
    m = w / 2
    step = 26
    for horizontal in (True, False):
        length = (x1 - x0 - 2 * w) if horizontal else (y1 - y0 - 2 * w)
        n = int(length // step)
        start = (length - (n - 1) * step) / 2
        for i in range(n):
            t = start + i * step
            for side in (0, 1):
                if horizontal:
                    cx, cy = x0 + w + t, (y0 + m if side == 0 else y1 - m)
                else:
                    cx, cy = (x0 + m if side == 0 else x1 - m), y0 + w + t
                if i % 2 == 0:
                    b.append('<polygon points="%s" fill="%s"/>' % (O.star(cx, cy, 7.5, 3.6, 8), GOLD))
                else:
                    b.append('<circle cx="%g" cy="%g" r="2.1" fill="%s"/>' % (cx, cy, GOLD))
    for cx, cy in ((x0 + m, y0 + m), (x1 - m, y0 + m), (x0 + m, y1 - m), (x1 - m, y1 - m)):
        b.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx - m, cy - m, w, w, GROUND, GOLD))
        b.append(rosette(cx, cy, m - 3, GOLD, 1.0))
    return "".join(b)


def quarter(cx, cy, r, sx, sy):
    """quarter medallion in an inner corner (sx, sy = direction into the page)"""
    shape = [(cx, cy)]
    for i in range(0, 91):
        t = math.radians(i)
        k = 1 - 0.07 * (1 - abs(math.cos(6 * t))) ** 1.5
        shape.append((cx + sx * r * k * math.cos(t), cy + sy * r * k * math.sin(t)))
    inner = [(cx, cy)] + [(cx + sx * r * 0.82 * math.cos(math.radians(i)), cy + sy * r * 0.82 * math.sin(math.radians(i))) for i in range(91)]
    return ('<polygon points="%s" fill="#072a20" stroke="%s" stroke-width="2"/>' % (pts(shape), GOLD) +
            '<polygon points="%s" fill="none" stroke="%s" stroke-width="0.7" stroke-dasharray="2 3"/>' % (pts(inner), GOLD) +
            rosette(cx + sx * r * 0.42, cy + sy * r * 0.42, r * 0.28, GOLD, 0.9))


def shamsa(cx, cy, rx, ry):
    outer = lobed(cx, cy, rx, ry, 28, 0.035)
    mid = lobed(cx, cy, rx - 10, ry - 10, 28, 0.035)
    inner = lobed(cx, cy, rx - 22, ry - 22, 28, 0.03)
    b = ['<polygon points="%s" fill="#06261d" stroke="%s" stroke-width="3.2"/>' % (pts(outer), GOLD),
         '<polygon points="%s" fill="none" stroke="%s" stroke-width="1"/>' % (pts(mid), GOLD),
         '<polygon points="%s" fill="none" stroke="%s" stroke-width="0.8" stroke-dasharray="1.5 4"/>' % (pts(inner), GOLD)]
    b.append(rosette(cx, cy, min(rx, ry) * 0.92, GOLD, 0.8, 0.16))      # faint rosette inside
    for d in (-1, 1):                                                   # pendants above and below
        py = cy + d * (ry + 30)
        b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.4"/>' % (cx, cy + d * ry, cx, py - d * 14, GOLD))
        b.append('<polygon points="%s" fill="#06261d" stroke="%s" stroke-width="1.8"/>' % (pts(lobed(cx, py, 22, 16, 10, 0.08, 240)), GOLD))
        b.append('<polygon points="%s" fill="%s"/>' % (O.star(cx, py, 10, 4.6, 8), GOLD))
        b.append('<polygon points="%s" fill="%s"/>' % (O.star(cx, py + d * 26, 5, 2.4, 4), GOLD))
    return "".join(b)


def defs(u):
    return """<defs>
  <radialGradient id="bg{u}" cx="50%" cy="45%" r="78%">
    <stop offset="0" stop-color="#145c47"/><stop offset="0.6" stop-color="#0c3e30"/><stop offset="1" stop-color="#051f18"/>
  </radialGradient>
  <linearGradient id="gold{u}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{g1}"/><stop offset="0.55" stop-color="{g2}"/><stop offset="1" stop-color="{g3}"/>
  </linearGradient>
  <pattern id="pt{u}" width="68" height="68" patternUnits="userSpaceOnUse">{tile}</pattern>
  <filter id="sh{u}" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity="0.55"/>
  </filter>
</defs>""".format(u=u, g1=G1, g2=G2, g3=G3, tile=tile())


def frame(u):
    b = ['<rect width="%d" height="%d" fill="url(#bg%s)"/>' % (VW, VH, u),
         '<rect width="%d" height="%d" fill="url(#pt%s)"/>' % (VW, VH, u),
         border_band(24, 24, VW - 24, VH - 24, 40)]
    for cx, cy, sx, sy in ((64, 64, 1, 1), (VW - 64, 64, -1, 1), (64, VH - 64, 1, -1), (VW - 64, VH - 64, -1, -1)):
        b.append(quarter(cx, cy, 120, sx, sy))
    return "".join(b)


def front():
    cx, cy = VW / 2, 418
    title = """
  <g filter="url(#sha)" font-family="Aref Ruqaa" font-weight="700" text-anchor="middle" direction="rtl" fill="url(#golda)">
    <text x="{cx}" y="{y1}" font-size="112">ثرائد</text>
    <text x="{cx}" y="{y2}" font-size="148">التقوى</text>
  </g>""".format(cx=cx, y1=cy - 34, y2=cy + 118)
    author = """
  <polygon points="{p}" fill="#06261d" stroke="{g}" stroke-width="1.8"/>
  <text x="{cx}" y="{ay}" text-anchor="middle" direction="rtl" font-family="Aref Ruqaa" font-weight="700" font-size="54" fill="url(#golda)" filter="url(#sha)">محمد عبدالله</text>
""".format(p=pts(lobed(cx, 805, 170, 46, 18, 0.06, 360)), g=GOLD, cx=cx, ay=822)
    return '<svg class="art" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">%s%s%s%s%s</svg>' % (
        VW, VH, defs("a"), frame("a"), shamsa(cx, cy, 214, 252), title, author)


def back():
    cx = VW / 2
    panel = lobed(cx, 452, 262, 300, 36, 0.018)
    b = [defs("b"), frame("b"),
         '<polygon points="%s" fill="#06261d" fill-opacity="0.82" stroke="%s" stroke-width="2.4"/>' % (pts(panel), GOLD),
         '<polygon points="%s" fill="none" stroke="%s" stroke-width="0.8"/>' % (pts(lobed(cx, 452, 250, 288, 36, 0.018)), GOLD),
         '<polygon points="%s" fill="%s"/>' % (O.star(cx, 152, 15, 7, 8), GOLD),
         '<g font-family="Aref Ruqaa" font-weight="700" text-anchor="middle" direction="rtl" fill="url(#goldb)" filter="url(#shb)">'
         '<text x="%g" y="835" font-size="54">ثرائد التقوى</text></g>' % cx,
         '<text x="%g" y="880" text-anchor="middle" direction="rtl" font-family="Amiri" font-size="26" fill="%s">محمد عبدالله</text>' % (cx, G1)]
    return '<svg class="art" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def main():
    paras = "".join("<p>%s</p>" % re.sub("[\u064B-\u0652\u0670]", "", t) for t in BACK_TEXT)   # no tashkeel on the cover
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Amiri"; font-weight: 400; src: url(../fonts/amiri-arabic-400-normal.woff2) format("woff2"); unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+200C-200E; }}
@font-face {{ font-family: "Amiri"; font-weight: 400; src: url(../fonts/amiri-latin-400-normal.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2000-206F; }}
@font-face {{ font-family: "Aref Ruqaa"; font-weight: 700; src: url(../fonts/aref-ruqaa-arabic-700-normal.woff2) format("woff2"); }}
@page {{ size: 170mm 240mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 170mm; height: 240mm; overflow: hidden; break-after: page; background: {ground}; }}
.art {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.text {{
  position: absolute; left: 37mm; right: 37mm; top: 50mm; height: 126mm;
  display: flex; flex-direction: column; justify-content: center;
}}
.text p {{
  margin: 0 0 3.5mm; text-align: justify; text-align-last: center;
  font-family: "Amiri", serif; font-size: 12.8pt; line-height: 2; color: #f6ead0;
}}
.text p:last-child {{ margin: 0; color: {g1}; }}
</style></head><body>
<div class="page">{front}</div>
<div class="page">{back}<div class="text">{paras}</div></div>
</body></html>""".format(ground=GROUND, g1=G1, front=front(), back=back(), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
