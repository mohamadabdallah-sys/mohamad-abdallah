# -*- coding: utf-8 -*-
"""Front and back cover (build/cover.html, two 170×240 mm pages)."""
import os, re
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

W, H = 170, 240   # mm


def background(uid):
    tile = O.pattern_tile(60, O.GOLD_LIGHT, 0.16)
    return """
<svg class="bg" viewBox="0 0 680 960" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="g{u}" cx="50%" cy="42%" r="75%">
      <stop offset="0" stop-color="#16684f"/><stop offset="0.55" stop-color="#0d4a39"/><stop offset="1" stop-color="#062a20"/>
    </radialGradient>
    <pattern id="p{u}" width="60" height="60" patternUnits="userSpaceOnUse">{tile}</pattern>
  </defs>
  <rect width="680" height="960" fill="url(#g{u})"/>
  <rect width="680" height="960" fill="url(#p{u})"/>
  <rect x="30" y="30" width="620" height="900" fill="none" stroke="{gold}" stroke-width="2.4"/>
  <rect x="40" y="40" width="600" height="880" fill="none" stroke="{gold}" stroke-width="0.9"/>
</svg>""".format(u=uid, tile=tile, gold=O.GOLD_LIGHT)


def corners():
    out = []
    for cls, fx, fy in (("tr", True, False), ("tl", False, False), ("br", True, True), ("bl", False, True)):
        out.append('<img class="corner %s" src="%s">' % (cls, O.data_uri(O.corner(80, O.GOLD_LIGHT, fx, fy))))
    return "".join(out)


def arch():
    # a pointed (mihrab) arch with a double gold outline
    path = "M60,600 L60,250 C60,140 160,80 230,20 C300,80 400,140 400,250 L400,600 Z"
    inner = "M74,586 L74,254 C74,152 168,96 230,40 C292,96 386,152 386,254 L386,586 Z"
    star = O.khatam(230, 150, 34, O.GOLD_LIGHT, "#0b4434", 1.6)
    return """
<svg class="arch" viewBox="0 0 460 620" xmlns="http://www.w3.org/2000/svg">
  <path d="{p}" fill="#072f24" fill-opacity="0.72" stroke="{g}" stroke-width="3"/>
  <path d="{i}" fill="none" stroke="{g}" stroke-width="1"/>
  {star}
</svg>""".format(p=path, i=inner, g=O.GOLD_LIGHT, star=star)


def main():
    divider = O.data_uri(O.divider(360, 30, O.GOLD_LIGHT).replace('fill="#fff"', 'fill="#0b4434"'))
    paras = "".join("<p>%s</p>" % re.sub("[\u064B-\u0652\u0670]", "", t) for t in BACK_TEXT)   # no tashkeel on the cover
    html = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>الغلاف</title>
<style>
@font-face {{ font-family: "Amiri"; font-weight: 400; src: url(../fonts/amiri-arabic-400-normal.woff2) format("woff2"); unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+200C-200E; }}
@font-face {{ font-family: "Amiri"; font-weight: 400; src: url(../fonts/amiri-latin-400-normal.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2000-206F; }}
@font-face {{ font-family: "Amiri"; font-weight: 700; src: url(../fonts/amiri-arabic-700-normal.woff2) format("woff2"); unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+200C-200E; }}
@font-face {{ font-family: "Amiri"; font-weight: 700; src: url(../fonts/amiri-latin-700-normal.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2000-206F; }}
@font-face {{ font-family: "Aref Ruqaa"; font-weight: 700; src: url(../fonts/aref-ruqaa-arabic-700-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Aref Ruqaa"; font-weight: 400; src: url(../fonts/aref-ruqaa-arabic-400-normal.woff2) format("woff2"); }}
@page {{ size: {W}mm {H}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; width: {W}mm; height: {H}mm; overflow: hidden; break-after: page; background: #0b4434; }}
.bg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.corner {{ position: absolute; width: 20mm; height: 20mm; }}
.corner.tr {{ top: 7.5mm; right: 7.5mm; }} .corner.tl {{ top: 7.5mm; left: 7.5mm; }}
.corner.br {{ bottom: 7.5mm; right: 7.5mm; }} .corner.bl {{ bottom: 7.5mm; left: 7.5mm; }}
.arch {{ position: absolute; left: 27.5mm; top: 33mm; width: 115mm; height: 155mm; }}
.front .title {{
  position: absolute; left: 0; right: 0; top: 92mm; text-align: center;
  font-family: "Aref Ruqaa", serif; font-weight: 700; color: #ecd08e;
  font-size: 60pt; line-height: 1.2;
  text-shadow: 0 0.6mm 1.2mm rgba(0,0,0,0.45);
}}
.front .title span {{ display: block; }}
.front .title .t2 {{ font-size: 76pt; }}
.front .div {{ position: absolute; left: 45mm; right: 45mm; top: 166mm; height: 8mm; background: url({divider}) center / contain no-repeat; }}
.front .author {{
  position: absolute; left: 0; right: 0; bottom: 27mm; text-align: center;
  font-family: "Aref Ruqaa", serif; font-weight: 700; font-size: 28pt; color: #f4e7c6;
}}
.front .author small {{ display: block; font-family: "Amiri", serif; font-weight: 400; font-size: 10.5pt; color: #d9bf83; margin-bottom: 1mm; letter-spacing: 0.3mm; }}
.back .panel {{
  position: absolute; left: 21mm; right: 21mm; top: 42mm; bottom: 56mm;
  border: 0.9pt solid #e2c27a; outline: 0.4pt solid #e2c27a; outline-offset: 1.6mm;
  background: rgba(4, 34, 26, 0.55);
  padding: 10mm 9mm; box-sizing: border-box;
  display: flex; flex-direction: column; justify-content: center;
}}
.back .panel p {{
  margin: 0 0 4mm; text-align: justify; text-align-last: center;
  font-family: "Amiri", serif; font-size: 14.8pt; line-height: 2.1; color: #f4e7c6;
}}
.back .panel p:last-child {{ margin: 0; color: #ecd08e; }}
.back .top {{ position: absolute; left: 45mm; right: 45mm; top: 27mm; height: 9mm; background: url({divider}) center / contain no-repeat; }}
.back .sig {{ position: absolute; left: 0; right: 0; bottom: 24mm; text-align: center; color: #ecd08e; }}
.back .sig .t {{ font-family: "Aref Ruqaa", serif; font-weight: 700; font-size: 22pt; line-height: 1.4; }}
.back .sig .a {{ font-family: "Amiri", serif; font-size: 12pt; color: #f4e7c6; }}
</style></head><body>
<div class="page front">
  {bg1}{corners}{arch}
  <div class="title"><span class="t1">ثرائد</span><span class="t2">التقوى</span></div>
  <div class="div"></div>
  <div class="author"><small>تأليف</small>محمد عبدالله</div>
</div>
<div class="page back">
  {bg2}{corners}
  <div class="top"></div>
  <div class="panel">{paras}</div>
  <div class="sig"><div class="t">ثرائد التقوى</div><div class="a">محمد عبدالله</div></div>
</div>
</body></html>""".format(W=W, H=H, divider=divider, bg1=background("a"), bg2=background("b"),
                         corners=corners(), arch=arch(), paras=paras)
    open(os.path.join(HERE, "build", "cover.html"), "w", encoding="utf8").write(html)


if __name__ == "__main__":
    main()
