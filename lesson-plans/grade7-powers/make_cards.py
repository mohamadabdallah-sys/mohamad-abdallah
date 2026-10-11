"""Printable cards for the lesson القوى وقوى العشرة -> بطاقات-القوى-وقوى-العشرة.pdf (A4).

usage: python3 make_cards.py   (needs Chromium via Playwright, like ../../grade7-book/pdf.js)
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
    """'2^{5} × 3^2' -> LTR math span with superscripts."""
    s = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"\^(.)", r"<sup>\1</sup>", s)
    return f'<bdi class="m" dir="ltr">{s}</bdi>'


def head(n, title, tag, color, extra=""):
    return f"""<div class="head" style="--c:{color}">
  <span class="no">{n}</span><h2>{title}</h2><span class="tag">{tag}</span>{extra}</div>"""


FOOT = '<div class="foot">القوى وقوى العشرة · الصف السابع – شعبة نور · المجموعة: ............ · الأسماء: ................................................</div>'

# ---------------------------------------------------------------- cards
fold = f"""
<section class="card full" style="--c:#1B3A7A">
{head(1, "النشاط 1 – طيّ الورقة", "الاستكشاف · حركي – جسدي", "#1B3A7A")}
<p class="lead">نطوي ورقة A4 من المنتصف مرّة بعد مرّة، ونعدّ الطبقات بعد كل طيّة.</p>
<ol class="steps">
  <li><b>الطاوي:</b> يطوي الورقة من المنتصف.</li>
  <li><b>العادّ:</b> يعدّ الطبقات بعد كل طيّة.</li>
  <li><b>المسجّل:</b> يكتب العدد في الجدول، ثم يكتبه على شكل قوّة للعدد 2.</li>
</ol>
<table class="grid">
  <tr><th>عدد الطيّات</th>{"".join(f"<td class='hd'>{k}</td>" for k in (0, 1, 2, 3, 4, 5, 10))}</tr>
  <tr><th>عدد الطبقات</th><td>1</td>{"<td></td>" * 6}</tr>
  <tr><th>على شكل قوّة للعدد 2</th><td>{m("2^0")}</td>{"<td></td>" * 6}</tr>
</table>
<div class="q"><span>1</span> ماذا يحدث لعدد الطبقات بعد كل طيّة؟ <i class="line"></i></div>
<div class="q"><span>2</span> ما العلاقة بين عدد الطيّات والأُس؟ <i class="line"></i></div>
<div class="q"><span>3</span> لماذا يصعب الطيّ بعد 6 أو 7 طيّات؟ كيف نكمل العمود 10 دون طيّ؟ <i class="line"></i></div>
<div class="box">بعد 10 طيّات: {m("2^{10}")} = ............ طبقة &nbsp;(تحقّق بالآلة الحاسبة)</div>
{FOOT}
</section>"""

rows2 = [("2^3 × 2^2", "2"), ("3^2 × 3^4", "3"), ("2^5 ÷ 2^2", "2"), ("(5^2)^3", "5")]
act2 = f"""
<section class="card full" style="--c:#0E7C7B">
{head(2, "النشاط 2 – من الكتابة المفكّكة إلى القاعدة", "الاستكشاف · رياضي – منطقي", "#0E7C7B")}
<p class="lead">فكّك كل قوّة إلى عوامل، عُدّ العوامل، ثم اكتب النتيجة قوّة واحدة.</p>
<div class="eg">مثال محلول: {m("2^3 × 2^2 = (2×2×2) × (2×2) = 2^5")} &nbsp; ← 5 عوامل</div>
<table class="work">
  <tr><th>العبارة</th><th>الكتابة المفكّكة</th><th>عدد العوامل</th><th>قوّة واحدة</th></tr>
  {"".join(f"<tr><td class='ex'>{m(q)}</td><td></td><td></td><td class='ans'>{m(b + '^{□}')}</td></tr>" for q, b in rows2)}
</table>
<h3>نستنتج القواعد (الأساس نفسه):</h3>
<div class="rules3">
  <div><b>جداء قوّتين</b>{m("a^m × a^n = a^{□}")}<small>ماذا نفعل بالأُسَّين؟ ........</small></div>
  <div><b>قسمة قوّتين</b>{m("a^m ÷ a^n = a^{□}")}<small>ماذا نفعل بالأُسَّين؟ ........</small></div>
  <div><b>قوّة القوّة</b>{m("(a^m)^n = a^{□}")}<small>ماذا نفعل بالأُسَّين؟ ........</small></div>
</div>
<p class="hint">💡 إذا تردّدت، اكتب العوامل كلّها وعُدّها، ثم تحقّق بالآلة الحاسبة.</p>
{FOOT}
</section>"""

act3 = f"""
<section class="card full" style="--c:#7A3E8E">
{head(3, "النشاط 3 – لغز الأُس صفر", "الاستكشاف · رياضي – منطقي", "#7A3E8E")}
<p class="lead">لاحظ: كلّما نقص الأُس بواحد نقسم على 3. أكمل الجدول.</p>
<table class="grid stair">
  <tr><th>القوّة</th>{"".join(f"<td class='hd'>{m(p)}</td>" for p in ("3^4", "3^3", "3^2", "3^1", "3^0"))}</tr>
  <tr><th>القيمة</th><td>81</td><td>27</td><td></td><td></td><td></td></tr>
</table>
<div class="q"><span>1</span> ما قيمة {m("3^0")} حسب النمط؟ <i class="line"></i></div>
<div class="q"><span>2</span> تحقّق بقاعدة القسمة: {m("3^2 ÷ 3^2 = 3^{□−□} = 3^{□}")} &nbsp; ومن جهة أخرى {m("9 ÷ 9 = ……")}</div>
<div class="q"><span>3</span> ماذا تستنتج؟ {m("a^0 = ……")} &nbsp;(بشرط {m("a ≠ 0")}) <i class="line"></i></div>
<div class="q"><span>4</span> هل يتغيّر الجواب لو بدأنا بالأساس 2 بدلًا من 3؟ جرّب: {m("2^3 = 8, 2^2 = …, 2^1 = …, 2^0 = …")}</div>
{FOOT}
</section>"""

expl = f"""
<section class="card full ref" style="--c:#0F2350">
{head("★", "بطاقة الشرح: القوى وقواعدها", "التفسير", "#0F2350")}
<div class="two">
  <div class="panel">
    <h3>التعريف</h3>
    <p>القوّة {m("a^n")} هي جداء <b>n</b> عاملًا كلٌّ منها يساوي <b>a</b>.<br>
    <b>a</b> الأساس، <b>n</b> الأُس.</p>
    <p class="big">{m("2^5 = 2 × 2 × 2 × 2 × 2 = 32")}</p>
    <p>وليس {m("2 × 5 = 10")}.</p>
    <p>نقرأ {m("a^2")} «مربّع a» و{m("a^3")} «مكعّب a».</p>
  </div>
  <div class="panel">
    <h3>حالتان خاصّتان</h3>
    <p>{m("a^1 = a")} &nbsp; مثل {m("7^1 = 7")}</p>
    <p>{m("a^0 = 1  (a ≠ 0)")} &nbsp; مثل {m("2026^0 = 1")}</p>
    <h3>إشارة القوّة (أساس سالب)</h3>
    <p>أُس زوجي ← موجبة: {m("(−2)^4 = 16")}</p>
    <p>أُس فردي ← سالبة: {m("(−2)^3 = −8")}</p>
  </div>
</div>
<div class="panel">
  <h3>قوى العشرة</h3>
  <p>{m("10^n")} هو العدد 1 متبوعًا بـ n أصفار: &nbsp; {m("10^3 = 1000")} &nbsp;·&nbsp; {m("10^6 = 1 000 000")}</p>
</div>
<table class="rules">
  <tr><th>الخاصّة</th><th>القاعدة</th><th>مثال</th></tr>
  <tr><td>جداء قوّتين</td><td>{m("a^m × a^n = a^{m+n}")}</td><td>{m("2^3 × 2^4 = 2^7 = 128")}</td></tr>
  <tr><td>قسمة قوّتين</td><td>{m("a^m ÷ a^n = a^{m−n}")}</td><td>{m("10^8 ÷ 10^5 = 10^3 = 1000")}</td></tr>
  <tr><td>قوّة القوّة</td><td>{m("(a^m)^n = a^{m×n}")}</td><td>{m("(3^2)^3 = 3^6 = 729")}</td></tr>
  <tr><td>قوّة الجداء</td><td>{m("a^n × b^n = (a × b)^n")}</td><td>{m("5^3 × 2^3 = 10^3 = 1000")}</td></tr>
  <tr><td>قوّة الحاصل</td><td>{m("(a ÷ b)^n = a^n ÷ b^n")}</td><td>{m("(6 ÷ 3)^4 = 6^4 ÷ 3^4 = 16")}</td></tr>
</table>
<div class="panel">
  <h3>أولويّات الحساب</h3>
  <p class="order"><span>الأقواس</span>←<span>القوى</span>←<span>الضرب والقسمة</span>←<span>الجمع والطرح</span></p>
  <p>{m("5^2 − 4 × 3 + 2^3 = 25 − 12 + 8 = 21")}</p>
</div>
<div class="warn"><b>⚠ انتبه!</b> {m("2^3 ≠ 2 × 3")} · {m("−2^4 = −16")} أمّا {m("(−2)^4 = 16")} · {m("(2 + 5)^2 ≠ 2^2 + 5^2")}</div>
</section>"""

challenge = f"""
<section class="card half" style="--c:#B7791F">
{head("🌙", "تحدّي المتميّزين: هل نصل إلى القمر؟", "توسيع", "#B7791F")}
<p class="lead">سماكة الورقة نحو <b>0.1 ملم</b>. كل طيّة تضاعف السماكة.<br>
لو استطعنا طيّها <b>42</b> مرّة، هل تصل سماكتها إلى القمر؟ (المسافة إلى القمر نحو <b>384 400 كلم</b>)</p>
<div class="q"><span>1</span> عدد الطبقات بعد 42 طيّة على شكل قوّة: <i class="line"></i></div>
<div class="q"><span>2</span> السماكة بالملّيمتر = {m("2^{42} × 0.1")} ≈ <i class="line"></i></div>
<div class="q"><span>3</span> حوّل إلى الكيلومتر ({m("1 km = 10^6 mm")}): <i class="line"></i></div>
<div class="q"><span>4</span> قارن بالمسافة إلى القمر: <i class="line"></i></div>
</section>"""

mistakes = f"""
<section class="card half" style="--c:#C2452F">
{head("!", "انتبه! أخطاء شائعة – اكتشف الخطأ وصحّحه", "النشاط التقييمي", "#C2452F")}
<table class="mist">
  <tr><th></th><th>العبارة</th><th>صحيحة أم خاطئة؟ لماذا؟</th><th>التصحيح</th></tr>
  <tr><td>1</td><td>{m("2^3 = 6")}</td><td></td><td></td></tr>
  <tr><td>2</td><td>{m("−2^4 = 16")}</td><td></td><td></td></tr>
  <tr><td>3</td><td>{m("(2 + 5)^2 = 2^2 + 5^2")}</td><td></td><td></td></tr>
  <tr><td>4</td><td>{m("2^3 × 3^2 = 6^5")}</td><td></td><td></td></tr>
</table>
</section>"""

homework = f"""
<section class="card half" style="--c:#2F7D46">
{head("🏠", "الواجب البيتي", "الختام", "#2F7D46")}
<p class="lead"><b>1)</b> أعد جدول «لغز الأُس صفر» بالأساس 5 بدلًا من 3:</p>
<table class="grid stair">
  <tr><th>القوّة</th>{"".join(f"<td class='hd'>{m(p)}</td>" for p in ("5^4", "5^3", "5^2", "5^1", "5^0"))}</tr>
  <tr><th>القيمة</th>{"<td></td>" * 5}</tr>
</table>
<div class="q">تحقّق بقاعدة القسمة: {m("5^2 ÷ 5^2 = ……")} &nbsp; هل تتغيّر النتيجة؟ <i class="line"></i></div>
<p class="lead"><b>2)</b> أكمل جدول طيّ الورقة حتى 10 طيّات (لمن لم يُنهِه في الصف).</p>
<p class="name">الاسم: ..................................................</p>
</section>"""

vocab = [("القوّة", "Power", "2^5"), ("الأساس", "Base", "2^5 : 2"), ("الأُس", "Exponent", "2^5 : 5"),
         ("المربّع", "Square", "a^2 = a × a"), ("المكعّب", "Cube", "a^3 = a × a × a"), ("قوى العشرة", "Powers of ten", "10^n")]
roles = [("الطاوي", "يطوي الورقة من المنتصف مرّة بعد مرّة", "#0E7C7B"), ("العادّ", "يعدّ الطبقات بعد كل طيّة", "#7A3E8E"),
         ("المسجّل", "يدوّن النتائج في الجدول", "#C2452F")]
small = f"""
<section class="smalls">
<h2 class="pg">بطاقات المصطلحات وأدوار المجموعة <small>(للقصّ)</small></h2>
<div class="sgrid">
{"".join(f'<div class="sc"><b>{a}</b><span>{e}</span>{m(x)}</div>' for a, e, x in vocab)}
{"".join(f'<div class="sc role" style="--c:{c}"><em>دور</em><b>{r}</b><span class="ar">{d}</span></div>' for r, d, c in roles)}
</div>
</section>"""

key = f"""
<section class="card full key" style="--c:#172231">
{head("✓", "مفتاح الإجابات (للمعلّم)", "", "#172231")}
<h3>النشاط 1</h3>
<p>الطبقات: 1، 2، 4، 8، 16، 32، 1024 ← {m("2^0, 2^1, 2^2, 2^3, 2^4, 2^5, 2^{10}")}. كل طيّة تضاعف عدد الطبقات، والأُس = عدد الطيّات.</p>
<h3>النشاط 2</h3>
<p>{m("2^3 × 2^2 = 2^5")} (5 عوامل) · {m("3^2 × 3^4 = 3^6")} (6 عوامل) · {m("2^5 ÷ 2^2 = 2^3")} (نختصر عاملين) · {m("(5^2)^3 = 5^6")} (3 مجموعات من عاملين)</p>
<p>{m("a^m × a^n = a^{m+n}")} نجمع · {m("a^m ÷ a^n = a^{m−n}")} نطرح · {m("(a^m)^n = a^{m×n}")} نضرب</p>
<h3>النشاط 3</h3>
<p>{m("3^2 = 9, 3^1 = 3, 3^0 = 1")} · {m("3^2 ÷ 3^2 = 3^{2−2} = 3^0")} و{m("9 ÷ 9 = 1")}، إذن {m("a^0 = 1  (a ≠ 0)")}. ومع الأساس 2: {m("4, 2, 1")}.</p>
<h3>التحدّي</h3>
<p>{m("2^{42} = 4 398 046 511 104")} طبقة · السماكة ≈ {m("439 804 651 110 mm ≈ 439 805 km")} &gt; 384 400 كلم ← نعم، تتجاوز المسافة إلى القمر.</p>
<h3>انتبه! أخطاء شائعة</h3>
<p>1) {m("2^3 = 8")} (القوّة ليست ضرب الأساس في الأُس) · 2) {m("−2^4 = −16")} (بلا أقواس الأُس يخصّ 2 وحده)<br>
3) {m("(2 + 5)^2 = 7^2 = 49")} وليس 29 (الأُس لا يتوزّع على الجمع) · 4) {m("2^3 × 3^2 = 8 × 9 = 72")} (أساسان وأُسّان مختلفان)</p>
<h3>الواجب</h3>
<p>{m("5^4 = 625, 5^3 = 125, 5^2 = 25, 5^1 = 5, 5^0 = 1")} · {m("5^2 ÷ 5^2 = 5^0 = 1")} ← النتيجة لا تتغيّر.</p>
</section>"""

CSS = """
@page { size: A4; margin: 10mm }
* { box-sizing: border-box }
body { margin: 0; font-family: "IBM Plex Sans Arabic", sans-serif; color: #172231; font-size: 15pt; line-height: 1.7 }
h2, h3, .no, .tag, th, b { font-family: "Readex Pro", "IBM Plex Sans Arabic", sans-serif }
.m { font-family: "Readex Pro", sans-serif; unicode-bidi: isolate; white-space: nowrap; font-weight: 500 }
sup { font-size: .68em; line-height: 0 }
.card { border: 2px solid var(--c); border-radius: 14px; padding: 7mm 8mm; position: relative; break-inside: avoid; overflow: hidden }
.full { height: 276mm; break-after: page; display: flex; flex-direction: column; gap: 6mm }
.half { height: 133mm; margin-bottom: 9mm; display: flex; flex-direction: column; gap: 2.6mm }
.half + .half { margin-bottom: 0 }
.half:first-child::after { content: "✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -";
  position: absolute; bottom: -7mm; right: 0; left: 0; color: #9AA5B4; font-size: 10pt; white-space: nowrap; overflow: hidden }
.pagehalves { height: 276mm; break-after: page; display: flex; flex-direction: column; justify-content: space-between }
.pagehalves .half { margin: 0; position: relative }
.pagehalves .half:first-child::after { content: "✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -";
  position: absolute; bottom: -6.5mm; right: 0; left: 0; color: #9AA5B4; font-size: 10pt; white-space: nowrap; overflow: hidden }
.head { display: flex; align-items: center; gap: 3mm; background: var(--c); color: #fff; margin: -7mm -8mm 1mm; padding: 4mm 8mm }
.head h2 { margin: 0; font-size: 17pt; flex: 1 }
.no { width: 10mm; height: 10mm; border-radius: 50%; background: #fff; color: var(--c); display: grid; place-items: center; font-weight: 700; font-size: 14pt; flex: none }
.tag { font-size: 10pt; background: rgba(255,255,255,.18); padding: 1mm 3mm; border-radius: 20px }
.lead { margin: 0; font-size: 14pt }
.steps { margin: 0; padding-inline-start: 7mm }
h3 { margin: 1mm 0 0; font-size: 13pt; color: var(--c) }
table { border-collapse: collapse; width: 100% }
th, td { border: 1.3px solid #B9C3D0; padding: 2mm; text-align: center }
th { background: color-mix(in srgb, var(--c) 12%, #fff); color: var(--c); font-size: 12pt }
.grid td { height: 20mm; font-size: 17pt }
.grid td.hd { height: 13mm; background: #F2F5F9; font-weight: 700 }
.stair td { height: 18mm }
.q { display: flex; align-items: baseline; gap: 2mm; flex-wrap: wrap }
.q span { width: 7mm; height: 7mm; border-radius: 50%; background: var(--c); color: #fff; display: inline-grid; place-items: center; font-size: 10pt; flex: none; transform: translateY(-1px) }
.q .line { flex: 1 1 100%; border-bottom: 1.3px dashed #9AA5B4; height: 9mm }
.box, .eg { background: color-mix(in srgb, var(--c) 9%, #fff); border-radius: 10px; padding: 3mm 4mm; font-size: 14pt }
.work td { height: 27mm; font-size: 17pt }
.work td.ex { width: 28%; font-weight: 700 } .work td.ans { width: 18%; color: var(--c) }
.rules3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm }
.rules3 div { border: 1.3px solid #B9C3D0; border-radius: 10px; padding: 5mm 3mm; display: flex; flex-direction: column; align-items: center; gap: 2mm; font-size: 17pt }
.rules3 small { font-size: 10.5pt; color: #4F5C6E }
.hint { margin: auto 0 0; color: #4F5C6E; font-size: 12pt }
.foot { margin-top: auto; font-size: 10pt; color: #7C8797; border-top: 1px solid #DCE2E9; padding-top: 2mm }
.arrows { text-align: center; color: #7A3E8E; font-weight: 700; direction: ltr; font-size: 14pt }
.ref { font-size: 14pt; gap: 3.5mm }
.ref .two { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm }
.panel { background: #F2F5F9; border-radius: 10px; padding: 2.5mm 4mm }
.panel p { margin: 1mm 0 }
.panel .big { font-size: 15pt; text-align: center }
.rules td { padding: 2.6mm; font-size: 14.5pt } .rules td:first-child { font-weight: 700; text-align: right }
.order span { background: #0F2350; color: #fff; padding: .5mm 3mm; border-radius: 20px; margin: 0 1mm; font-size: 11.5pt }
.warn { background: #FBE9E5; color: #8E2B1A; border-radius: 10px; padding: 2.5mm 4mm }
.mist td { height: 20mm; font-size: 15pt } .mist td:first-child { width: 8mm; font-weight: 700; color: var(--c) }
.mist td:nth-child(2) { width: 30%; font-weight: 700 }
.name { margin: auto 0 0; color: #4F5C6E }
.smalls { break-after: page }
.pg { font-size: 17pt; color: #0F2350; margin: 0 0 4mm } .pg small { font-size: 11pt; color: #7C8797 }
.sgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; border: 1.5px dashed #9AA5B4 }
.sc { height: 84mm; border: 1.5px dashed #9AA5B4; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4mm; padding: 5mm; text-align: center }
.sc b { font-size: 28pt; color: #0F2350 } .sc span { font-size: 15pt; color: #4F5C6E } .sc .m { font-size: 20pt; color: #0E7C7B }
.sc.role { background: color-mix(in srgb, var(--c) 10%, #fff) } .sc.role b { color: var(--c) } .sc.role em { font-style: normal; font-size: 11pt; color: #7C8797 }
.sc .ar { font-size: 14pt }
.key { font-size: 14pt; gap: 2.5mm } .key p { margin: 0 }
"""

html = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>بطاقات القوى وقوى العشرة</title>
<style>{font_css()}{CSS}</style></head><body>
{fold}{act2}{act3}{expl}
<div class="pagehalves">{challenge}{mistakes}</div>
<div class="pagehalves">{homework}{homework}</div>
{small}{key}
</body></html>"""

out_html = os.path.join(HERE, "cards.html")  # temporary, removed after printing
open(out_html, "w", encoding="utf-8").write(html)
JS = """const pw = require("/opt/node22/lib/node_modules/playwright");
(async () => { const b = await pw.chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + process.argv[1], { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: process.argv[2], format: "A4", printBackground: true, preferCSSPageSize: true }); await b.close(); })();"""
subprocess.run(["node", "-e", JS, out_html, os.path.join(HERE, "بطاقات-القوى-وقوى-العشرة.pdf")], check=True)
print("wrote cards PDF")
os.remove(out_html)
