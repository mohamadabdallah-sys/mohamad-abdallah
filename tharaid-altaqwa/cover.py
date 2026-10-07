# -*- coding: utf-8 -*-
"""Front and back cover (build/cover.html, two 170×240 mm pages): a modern, minimal design —
a deep ink ground with a soft warm glow, one thin gold ring, a Kufi display title and a clean sans-serif text."""
import os, re

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
INK = "#0d1720"
GOLD = "#d6b06a"
CREAM = "#f3ece0"


def plain(s):
    """no tashkeel anywhere on the cover"""
    return re.sub("[ً-ْٰ]", "", s)


def defs(u):
    return """<defs>
  <linearGradient id="bg{u}" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#16283a"/><stop offset="0.55" stop-color="#0f1c28"/><stop offset="1" stop-color="#091118"/>
  </linearGradient>
  <radialGradient id="glow{u}" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#e3b768" stop-opacity="0.30"/>
    <stop offset="0.45" stop-color="#c9954a" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#c9954a" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ring{u}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#f4dca4"/><stop offset="0.5" stop-color="{g}"/><stop offset="1" stop-color="#8f6c33"/>
  </linearGradient>
</defs>""".format(u=u, g=GOLD)


def front():
    cx, cy, r = VW / 2, 392, 232
    b = [defs("a"),
         '<rect width="%d" height="%d" fill="url(#bga)"/>' % (VW, VH),
         '<circle cx="%g" cy="%g" r="%g" fill="url(#glowa)"/>' % (cx, cy, r * 1.55),
         # the ring, open at the bottom where a fine line drops towards the author's name
         '<path d="M %.1f %.1f A %g %g 0 1 1 %.1f %.1f" fill="none" stroke="url(#ringa)" stroke-width="1.6"/>'
         % (cx - 14, cy + r - 0.4, r, r, cx + 14, cy + r - 0.4),
         '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.2"/>' % (cx, cy + r - 26, cx, 790, GOLD),
         '<circle cx="%g" cy="%g" r="4.2" fill="%s"/>' % (cx, cy + r - 26, GOLD),
         # one small sphere riding on the ring
         '<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (cx + r * 0.7071, cy - r * 0.7071, GOLD),
         '<circle cx="%.1f" cy="%.1f" r="15" fill="none" stroke="%s" stroke-opacity="0.35" stroke-width="0.8"/>'
         % (cx + r * 0.7071, cy - r * 0.7071, GOLD)]
    return '<svg class="art" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def back():
    b = [defs("b"),
         '<rect width="%d" height="%d" fill="url(#bgb)"/>' % (VW, VH),
         # the front's ring, glimpsed at the corner
         '<circle cx="%g" cy="%g" r="300" fill="url(#glowb)"/>' % (VW - 40, 40),
         '<circle cx="%g" cy="%g" r="210" fill="none" stroke="url(#ringb)" stroke-opacity="0.55" stroke-width="1.4"/>' % (VW - 20, 20)]
    return '<svg class="art" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VW, VH, "".join(b))


def main():
    paras = "".join("<p>%s</p>" % plain(t) for t in BACK_TEXT)
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Reem Kufi"; font-weight: 700; src: url(../fonts/reem-kufi-arabic-700-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Plex Arabic"; font-weight: 300; src: url(../fonts/ibm-plex-sans-arabic-arabic-300-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Plex Arabic"; font-weight: 400; src: url(../fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Plex Arabic"; font-weight: 500; src: url(../fonts/ibm-plex-sans-arabic-arabic-500-normal.woff2) format("woff2"); }}
@page {{ size: 170mm 240mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: 170mm; height: 240mm; overflow: hidden; break-after: page; background: {ink}; }}
.art {{ position: absolute; inset: 0; width: 100%; height: 100%; }}

/* front */
.title {{
  position: absolute; left: 0; right: 0; top: 60mm; height: 76mm;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  font-family: "Reem Kufi", sans-serif; font-weight: 700; color: {cream}; line-height: 1.12;
}}
.title .t1 {{ font-size: 58pt; }}
.title .t2 {{ font-size: 80pt; }}
.author {{
  position: absolute; left: 0; right: 0; top: 201mm; text-align: center;
  font-family: "Plex Arabic", sans-serif; font-weight: 500; font-size: 19pt; color: {gold};
}}

/* back */
.text {{
  position: absolute; left: 26mm; right: 26mm; top: 52mm; height: 120mm;
  display: flex; flex-direction: column; justify-content: center;
}}
.text::before {{ content: ""; display: block; width: 14mm; border-top: 1.4pt solid {gold}; margin-bottom: 7mm; }}
.text p {{
  margin: 0 0 4mm; text-align: justify;
  font-family: "Plex Arabic", sans-serif; font-weight: 300; font-size: 12.6pt; line-height: 2.05; color: #e6e0d4;
}}
.text p:last-child {{ margin: 0; font-weight: 400; color: {gold}; }}
.sign {{
  position: absolute; right: 26mm; left: 26mm; bottom: 22mm;
  display: flex; align-items: baseline; justify-content: space-between;
  border-top: 0.6pt solid rgba(214,176,106,0.45); padding-top: 5mm;
}}
.sign .bt {{ font-family: "Reem Kufi", sans-serif; font-weight: 700; font-size: 19pt; color: {cream}; }}
.sign .ba {{ font-family: "Plex Arabic", sans-serif; font-weight: 400; font-size: 11pt; color: {gold}; }}
</style></head><body>
<div class="page">{front}
  <div class="title"><div class="t1">ثرائد</div><div class="t2">التقوى</div></div>
  <div class="author">محمد عبدالله</div>
</div>
<div class="page">{back}<div class="text">{paras}</div>
  <div class="sign"><span class="bt">ثرائد التقوى</span><span class="ba">محمد عبدالله</span></div>
</div>
</body></html>""".format(ink=INK, cream=CREAM, gold=GOLD, front=front(), back=back(), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
