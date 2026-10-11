"""Printable cards for the lesson إشارة ثلاثي الحدود -> بطاقات-إشارة-ثلاثي-الحدود.pdf (A4).

usage: python3 figs.py && python3 make_cards.py   (needs Chromium via Playwright)
"""
import base64
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "..", "..", "grade7-book")


def font_css():
    """Inline the grade-7 book's Arabic/Latin fonts (Readex Pro, IBM Plex Sans Arabic)."""
    css = open(os.path.join(BOOK, "fonts", "fonts.css"), encoding="utf-8").read()
    out = []
    for subset, blk in re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face\s*\{.*?\})", css, re.S):
        if subset not in ("arabic", "latin"):
            continue
        url = re.search(r"url\((https://[^)]+)\)", blk).group(1)
        data = open(os.path.join(BOOK, "fonts", os.path.basename(url)), "rb").read()
        out.append(blk.replace(url, "data:font/woff2;base64," + base64.b64encode(data).decode()))
    return "\n".join(out)


def m(s):
    """'x^2 − 5x + 6' -> LTR math span with superscripts."""
    s = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"\^(.)", r"<sup>\1</sup>", s)
    return f'<bdi class="m" dir="ltr">{s}</bdi>'


def fig(key):
    return f'<div class="fig">{open(os.path.join(HERE, "figs", key + ".svg"), encoding="utf-8").read()}</div>'


def sign(xs, f=None, label="f(x)"):
    """Sign table, x increasing left to right; f = [interval, point, interval, ...] or None (blank)."""
    n = len(xs)
    f = f or [""] * (2 * n - 3)
    top = "".join(f"<td class='xv'>{m(x)}</td>" + ("<td></td>" if i < n - 1 else "") for i, x in enumerate(xs))
    bot = "<td></td>"
    for j, v in enumerate(f):
        cls = {"+": "p", "−": "n"}.get(v, "z")
        bot += f"<td class='{cls}{' pt' if j % 2 else ''}'>{v}</td>"
    bot += "<td></td>"
    return f"""<table class="sign" dir="ltr"><tr><th>{m('x')}</th>{top}</tr><tr><th>{m(label)}</th>{bot}</tr></table>"""


def values(fn, xs, label="f(x)", blank=False):
    cells = "".join(f"<td>{str(x).replace('-', '−')}</td>" for x in xs)
    vals = "".join("<td></td>" if blank else
                   f"<td class='{'p' if fn(x) > 0 else 'n' if fn(x) < 0 else 'z'}'>{str(fn(x)).replace('-', '−')}</td>" for x in xs)
    return f"""<table class="vals" dir="ltr"><tr><th>{m('x')}</th>{cells}</tr><tr><th>{m(label)}</th>{vals}</tr></table>"""


def head(n, title, tag, color):
    return f"""<div class="head" style="--c:{color}"><span class="no">{n}</span><h2>{title}</h2><span class="tag">{tag}</span></div>"""


NAME = '<div class="foot">الاسم: ............................................ &nbsp; الصف: ............ &nbsp; التاريخ: ............</div>'
PAIR = '<div class="foot">الثنائي: ............................................ و ............................................</div>'
LINE = '<i class="line"></i>'

# ---------------------------------------------------------------- cards
warm = f"""
<section class="card half" style="--c:#1F6F8B">
{head(1, "بطاقة التمهيد – نتذكّر", "فرديّ · 10 د", "#1F6F8B")}
<div class="q"><span>1</span> حلّ المعادلة {m("x^2 − 5x + 6 = 0")}. {LINE}</div>
<div class="q"><span>2</span> احسب المميّز {m("Δ")} للمعادلة {m("2x^2 + x + 3 = 0")}. ماذا تستنتج؟ {LINE}</div>
<div class="q"><span>3</span> أكمل جدول إشارة {m("2x − 4")}:</div>
{sign(["−∞", "…", "+∞"], label="2x − 4")}
{NAME}
</section>"""

explore = f"""
<section class="card full" style="--c:#1F6F8B">
{head(2, "بطاقة الاستكشاف (أ) – المنحنى ومحور الفواصل", "استقصاء موجّه · 10 د", "#1F6F8B")}
<div class="two">
  <div>{fig("f1")}<p class="cap">{m("f(x) = x^2 − x − 6")}</p></div>
  <div class="qs">
    <div class="q"><span>1</span> أين يقطع المنحنى محور الفواصل؟ {LINE}</div>
    <div class="q"><span>2</span> تحقّق بالحساب: {m("f(−2) = ……")} و {m("f(3) = ……")}</div>
    <div class="q"><span>3</span> متى يقع المنحنى <b class="pc">فوق</b> المحور؟ ما إشارة {m("f(x)")} عندها؟ {LINE}</div>
    <div class="q"><span>4</span> متى يقع المنحنى <b class="nc">تحت</b> المحور؟ ما إشارة {m("f(x)")} عندها؟ {LINE}</div>
  </div>
</div>
<h3>أكمل جدول إشارة {m("x^2 − x − 6")}:</h3>
{sign(["−∞", "…", "…", "+∞"])}
<div class="box">الاستنتاج: {m("f(x) < 0")} عندما ...................................... &nbsp;و {m("f(x) > 0")} عندما ......................................</div>
{PAIR}
</section>"""

funcs = [("x^2 − 2x − 3", "a = 1 , b = −2 , c = −3"), ("x^2 − 2x + 1", "a = 1 , b = −2 , c = 1"), ("x^2 − 2x + 3", "a = 1 , b = −2 , c = 3")]
pair = f"""
<section class="card full" style="--c:#6C4AB6">
{head(3, "بطاقة الاستكشاف (ب) – عمل ثنائي: ثلاث دوال", "عمل ثنائي · 12 د", "#6C4AB6")}
<p class="lead">لكلّ دالّة: احسب {m("Δ")}، حدّد عدد نقاط التقاطع مع محور الفواصل، وصِف إشارة الدالّة (يمكنكم التحقّق في GeoGebra).</p>
<table class="work">
  <tr><th>الدالّة</th><th>{m("Δ = b^2 − 4ac")}</th><th>عدد نقاط التقاطع</th><th>إشارة الدالّة</th></tr>
  {"".join(f"<tr><td class='ex'>{m(f)}<small>{m(c)}</small></td><td></td><td></td><td></td></tr>" for f, c in funcs)}
</table>
<h3>جداول الإشارة:</h3>
<div class="tabs3">
  {"".join(f"<div><p>{m(f)}</p>{sign(['−∞', '', '', '+∞'] if k == 0 else ['−∞', '', '+∞'] if k == 1 else ['−∞', '+∞'])}</div>" for k, (f, c) in enumerate(funcs))}
</div>
<div class="box">ماذا تلاحظون؟ متى تأخذ الدالّة إشارة {m("a")}؟ ............................................................................................................</div>
{PAIR}
</section>"""

f1 = lambda x: x * x - x - 6
support = f"""
<section class="card full sup-card" style="--c:#2F7D46">
{head("🤝", "بطاقة دعم – جدول قيم جاهز", "للمتعثّرين", "#2F7D46")}
<p class="lead">اقرأ الجدول: {m("f(x) = 0")} ← جذر · <b class="pc">موجبة</b> ← فوق المحور · <b class="nc">سالبة</b> ← تحته.</p>
<p class="cap">{m("f(x) = x^2 − x − 6")}</p>
{values(f1, range(-3, 5))}
<div class="three-vals">
  <div><p class="cap">{m("x^2 − 2x − 3")}</p>{values(lambda x: x * x - 2 * x - 3, range(-2, 5))}</div>
  <div><p class="cap">{m("x^2 − 2x + 1")}</p>{values(lambda x: x * x - 2 * x + 1, range(-2, 5))}</div>
  <div><p class="cap">{m("x^2 − 2x + 3")}</p>{values(lambda x: x * x - 2 * x + 3, range(-2, 5))}</div>
</div>
</section>"""

enrich = f"""
<section class="card h-enrich" style="--c:#B7791F">
{head("🚀", "بطاقة إثراء – ماذا يتغيّر إذا كان a < 0؟", "للمتفوّقين", "#B7791F")}
<div class="q"><span>1</span> احسب {m("Δ")} للدالّة {m("g(x) = −x^2 + x + 6")} وجد جذريها. {LINE}</div>
<div class="q"><span>2</span> قارن {m("g(x)")} مع {m("f(x) = x^2 − x − 6")}: ماذا تلاحظ؟ ({m("g(x) = −f(x)")}) {LINE}</div>
<div class="q"><span>3</span> أكمل جدول إشارة {m("g(x)")}:</div>
{sign(["−∞", "…", "…", "+∞"], label="g(x)")}
<div class="q" style="margin-bottom:2mm"><span>4</span> هل تبقى القاعدة «إشارة {m("a")} خارج الجذرين» صحيحة؟ {LINE}</div>
</section>"""

summary = f"""
<section class="card h-sum" style="--c:#123B4A">
{head("★", "الخلاصة – إشارة ثلاثي الحدود ax² + bx + c", "للدفتر", "#123B4A")}
<div class="rule">ثلاثي الحدود يأخذ <b>إشارة a</b> دائمًا، إلّا <b>بين الجذرين</b> عندما {m("Δ > 0")}.</div>
<div class="cases">
  <div><b>{m("Δ > 0")}</b> جذران {m("x_1 < x_2")}{sign(["−∞", "x₁", "x₂", "+∞"], ["إشارة a", "0", "عكس إشارة a", "0", "إشارة a"])}</div>
  <div><b>{m("Δ = 0")}</b> جذر مضاعف {m("x_0 = −b/2a")}{sign(["−∞", "x₀", "+∞"], ["إشارة a", "0", "إشارة a"])}</div>
  <div><b>{m("Δ < 0")}</b> لا جذور{sign(["−∞", "+∞"], ["إشارة a"])}</div>
</div>
</section>""".replace("x_1", "x₁").replace("x_2", "x₂").replace("x_0", "x₀")

hw = f"""
<section class="card full" style="--c:#1F6F8B">
{head("🏠", "الواجب البيتي", "الختام", "#1F6F8B")}
<div class="q"><span>1</span> ادرس إشارة {m("2x^2 − 3x − 2")} (احسب {m("Δ")}، الجذرين، ثم جدول الإشارة).</div>
{sign(["−∞", "…", "…", "+∞"], label="2x²−3x−2")}
<div class="q"><span>2</span> ادرس إشارة {m("x^2 + 6x + 9")}.</div>
{sign(["−∞", "…", "+∞"], label="x²+6x+9")}
<div class="sup"><b>بطاقة دعم:</b> أكمل جدول إشارة {m("x^2 − 9")} &nbsp;(تلميح: {m("x^2 − 9 = 0")} عندما {m("x = −3")} أو {m("x = 3")})
{sign(["−∞", "−3", "3", "+∞"], label="x²−9")}</div>
{NAME}
</section>"""

key = f"""
<section class="card full key" style="--c:#172231">
{head("✓", "مفتاح الإجابات (للمعلّم)", "", "#172231")}
<h3>التمهيد</h3>
<p>1) {m("Δ = 25 − 24 = 1")}، الحلّان {m("x = 2")} و {m("x = 3")}. &nbsp; 2) {m("Δ = 1 − 24 = −23 < 0")} ← لا حلول. &nbsp; 3) {m("2x − 4")}: سالب ثم {m("0")} عند {m("x = 2")} ثم موجب.</p>
<h3>الاستكشاف (أ)</h3>
<p>الجذران {m("−2")} و {m("3")} ({m("f(−2) = f(3) = 0")}). {m("f(x) > 0")} عندما {m("x < −2")} أو {m("x > 3")}، و {m("f(x) < 0")} عندما {m("−2 < x < 3")}.</p>
{sign(["−∞", "−2", "3", "+∞"], ["+", "0", "−", "0", "+"])}
<h3>الاستكشاف (ب)</h3>
<p>{m("x^2 − 2x − 3")}: {m("Δ = 16")}، نقطتان {m("−1")} و {m("3")}، سالبة بينهما وموجبة خارجهما. &nbsp;
{m("x^2 − 2x + 1")}: {m("Δ = 0")}، نقطة واحدة {m("1")}، موجبة وتنعدم عند {m("1")}. &nbsp;
{m("x^2 − 2x + 3")}: {m("Δ = −8")}، لا تقاطع، موجبة دائمًا.</p>
<h3>الإثراء</h3>
<p>{m("Δ = 1 + 24 = 25")}، الجذران {m("−2")} و {m("3")}؛ {m("g = −f")} فتنقلب الإشارات: {m("g(x) > 0")} بين الجذرين و {m("g(x) < 0")} خارجهما (إشارة {m("a = −1")} خارج الجذرين).</p>
<h3>التقييم الشفهي</h3>
<p>{m("x^2 − 4x + 3")}: {m("Δ = 4")}، الجذران {m("1")} و {m("3")}، سالبة بينهما وموجبة خارجهما. &nbsp; {m("−x^2 + 2x − 5")}: {m("Δ = −16 < 0")} و {m("a = −1 < 0")} ← سالبة دائمًا.</p>
<h3>الواجب</h3>
<p>{m("2x^2 − 3x − 2")}: {m("Δ = 9 + 16 = 25")}، الجذران {m("x = (3 − 5)/4 = −1/2")} و {m("x = (3 + 5)/4 = 2")}:</p>
{sign(["−∞", "−1/2", "2", "+∞"], ["+", "0", "−", "0", "+"], label="2x²−3x−2")}
<p>{m("x^2 + 6x + 9 = (x + 3)^2")}: {m("Δ = 0")}، الجذر {m("−3")}، موجبة وتنعدم عند {m("−3")}. &nbsp; {m("x^2 − 9")}: موجبة خارج {m("[−3 ; 3]")} وسالبة بين {m("−3")} و {m("3")}.</p>
</section>"""

CSS = """
@page { size: A4; margin: 10mm }
* { box-sizing: border-box }
body { margin: 0; font-family: "IBM Plex Sans Arabic", sans-serif; color: #172231; font-size: 14pt; line-height: 1.65 }
h2, h3, .no, .tag, th, b { font-family: "Readex Pro", "IBM Plex Sans Arabic", sans-serif }
.m { font-family: "Readex Pro", sans-serif; unicode-bidi: isolate; white-space: nowrap; font-weight: 500 }
sup { font-size: .68em; line-height: 0 }
.card { border: 2px solid var(--c); border-radius: 14px; padding: 7mm 8mm; position: relative; overflow: hidden; break-inside: avoid }
.full { height: 276mm; break-after: page; display: flex; flex-direction: column; gap: 4.5mm }
.half { height: 133mm; display: flex; flex-direction: column; gap: 3mm }
.page { height: 276mm; break-after: page; display: flex; flex-direction: column; justify-content: space-between }
.page .half:first-child::after { content: "✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -";
  position: absolute; bottom: -6.5mm; right: 0; left: 0; color: #9AA5B4; font-size: 10pt; white-space: nowrap; overflow: hidden }
.page .half, .page .h-enrich { overflow: visible }
.h-enrich { height: 118mm; display: flex; flex-direction: column; gap: 3mm }
.h-sum { height: 148mm; display: flex; flex-direction: column; gap: 3mm }
.page .h-enrich::after { content: "✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"; position: absolute; bottom: -7mm; right: 0; left: 0; color: #9AA5B4; font-size: 10pt; white-space: nowrap; overflow: hidden }
.sup-card .vals th, .sup-card .vals td { font-size: 15pt; padding: 2.5mm 1mm }
.sup-card .three-vals .cap { font-size: 14pt; margin-top: 4mm }
.sup-card { gap: 3mm }
.head { display: flex; align-items: center; gap: 3mm; background: var(--c); color: #fff; margin: -7mm -8mm 1mm; padding: 3.5mm 8mm; border-radius: 12px 12px 0 0 }
.head h2 { margin: 0; font-size: 16pt; flex: 1 }
.no { width: 10mm; height: 10mm; border-radius: 50%; background: #fff; color: var(--c); display: grid; place-items: center; font-weight: 700; font-size: 13pt; flex: none }
.tag { font-size: 10pt; background: rgba(255,255,255,.18); padding: 1mm 3mm; border-radius: 20px }
.lead { margin: 0 }
h3 { margin: 0; font-size: 13pt; color: var(--c) }
.q { display: flex; align-items: baseline; gap: 2mm; flex-wrap: wrap }
.q > span { width: 7mm; height: 7mm; border-radius: 50%; background: var(--c); color: #fff; display: inline-grid; place-items: center; font-size: 10pt; flex: none }
.q .line { flex: 1 1 100%; border-bottom: 1.3px dashed #9AA5B4; height: 8mm }
table { border-collapse: collapse }
.sign { margin: 1mm auto; width: 100%; max-width: 170mm }
.sign th { width: 24mm; background: #EDF3F5; border: 1.4px solid #8E9AAB; font-size: 13pt; padding: 1.5mm }
.sign td { border-top: 1.4px solid #8E9AAB; border-bottom: 1.4px solid #8E9AAB; height: 11mm; text-align: center; font-size: 15pt; font-weight: 700; min-width: 8mm }
.sign td:last-child { border-right: 1.4px solid #8E9AAB }
.sign td.xv { color: #123B4A }
.sign td.pt { border-left: 1px dashed #B9C3D0; border-right: 1px dashed #B9C3D0 }
.sign td.p { color: #2F7D46 } .sign td.n { color: #C2452F }
.sign td:not(.xv) { font-size: 12pt }
.sign td.p, .sign td.n, .sign td.z { font-size: 15pt }
.sign tr:last-child td { font-size: 11pt }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; align-items: center }
.fig svg { width: 100%; height: auto; border: 1px solid #DCE2E9; border-radius: 8px }
.cap { text-align: center; margin: 1mm 0; font-size: 14pt }
.qs { display: flex; flex-direction: column; gap: 3mm }
.pc { color: #2F7D46 } .nc { color: #C2452F }
.box, .rule, .sup { background: color-mix(in srgb, var(--c) 9%, #fff); border-radius: 10px; padding: 3mm 4mm }
.rule { font-size: 15pt; text-align: center }
.work { width: 100% }
.work th, .work td { border: 1.3px solid #B9C3D0; padding: 2mm; text-align: center }
.work th { background: color-mix(in srgb, var(--c) 12%, #fff); color: var(--c); font-size: 12pt }
.work td { height: 24mm } .work td.ex { width: 30%; font-size: 15pt; font-weight: 700 }
.work td.ex small { display: block; font-size: 9.5pt; color: #5B6878; font-weight: 400 }
.tabs3 { display: flex; flex-direction: column; gap: 1mm } .tabs3 p { margin: 0; font-weight: 700 }
.vals { width: 100%; margin: 0 auto }
.vals th, .vals td { border: 1.3px solid #B9C3D0; text-align: center; padding: 1mm; font-size: 12.5pt }
.vals th { background: #EDF3F5; width: 16mm }
.vals td.p { color: #2F7D46; font-weight: 700 } .vals td.n { color: #C2452F; font-weight: 700 } .vals td.z { font-weight: 700; background: #FFF6E0 }
.three-vals { display: grid; grid-template-columns: 1fr; gap: 0 }
.three-vals .cap { margin: 1.5mm 0 .5mm; font-size: 12.5pt }
.cases { display: flex; flex-direction: column; gap: 2mm }
.cases > div { background: #F2F5F8; border-radius: 10px; padding: 1.5mm 3mm }
.cases .sign { margin: .5mm auto } .cases .sign td { height: 9mm } .cases .sign th { padding: 1mm }
.cases .sign tr:last-child td { font-size: 10.5pt; color: #2F7D46 }
.foot { margin-top: auto; font-size: 10.5pt; color: #7C8797; border-top: 1px solid #DCE2E9; padding-top: 2mm }
.key { font-size: 12.5pt; gap: 2mm } .key p { margin: 0 }
.key .sign { max-width: 120mm }
"""

html = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>بطاقات إشارة ثلاثي الحدود</title>
<style>{font_css()}{CSS}</style></head><body>
<div class="page">{warm}{warm}</div>
{explore}{pair}
{support}
<div class="page">{enrich}{summary}</div>
{hw}
{key}
</body></html>"""

out_html = os.path.join(HERE, "cards.html")  # temporary, removed after printing
open(out_html, "w", encoding="utf-8").write(html)
JS = """const pw = require("/opt/node22/lib/node_modules/playwright");
(async () => { const b = await pw.chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + process.argv[1], { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: process.argv[2], format: "A4", printBackground: true, preferCSSPageSize: true }); await b.close(); })();"""
subprocess.run(["node", "-e", JS, out_html, os.path.join(HERE, "بطاقات-إشارة-ثلاثي-الحدود.pdf")], check=True)
os.remove(out_html)
print("wrote cards PDF")
