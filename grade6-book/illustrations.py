# -*- coding: utf-8 -*-
"""Hand-built SVG illustrations for the grade-6 lessons. Colours come from CSS classes (theme-aware)."""
import re


def _svg(body, vb="0 0 360 220"):
    return f'<svg class="il" viewBox="{vb}" direction="ltr" role="img" aria-hidden="true">{body}</svg>'


def _t(x, y, s, cls="lt", anchor="middle"):
    d = ' direction="rtl"' if re.search("[\u0600-\u06FF]", s) else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{d}>{s}</text>'


def naturals():
    heads = [("مليارات", "f2"), ("ملايين", "f1"), ("ألوف", "f2"), ("وحدات", "f1")]
    digits = "2 345 678 901".replace(" ", "")
    out = []
    for i, (h, c) in enumerate(heads):
        x = 20 + i * 82
        out.append(f'<rect class="{c} st" x="{x}" y="40" width="80" height="34" rx="6"/>' + _t(x + 40, 62, h, "lt sm"))
    for j, d in enumerate(digits.rjust(12)):
        x = 20 + j * 27.3
        if d != " ":
            out.append(f'<rect class="f3 st" x="{x + 2}" y="84" width="24" height="34" rx="4"/>' + _t(x + 14, 107, d))
    return _svg("".join(out) + '''
  <path class="ln" d="M20 132 H348"/>''' + _t(184, 160, "2 345 678 901", "lt big acc") +
                _t(184, 196, "نقسم الأرقام حلقات من ثلاثة، ونقرأ من اليسار", "lt sm"))


def order():
    steps = [("( )", "الأقواس"), ("2³", "القوى"), ("× ÷", "الضرب والقسمة"), ("+ −", "الجمع والطرح")]
    out = []
    for i, (s, n) in enumerate(steps):
        y = 30 + i * 42
        x = 44 + i * 30
        out.append(f'<rect class="{"f1" if i % 2 == 0 else "f2"} st" x="{x}" y="{y}" width="180" height="36" rx="8"/>'
                   + _t(x + 30, y + 24, s, "lt acc") + _t(x + 120, y + 24, n, "lt sm"))
        out.append(f'<circle class="dot" cx="{x - 14}" cy="{y + 18}" r="11"/>' + _t(x - 14, y + 23, str(i + 1), "lt sm inv"))
    return _svg("".join(out) + _t(180, 210, "2 + (3 + 5) × 4 = 2 + 8 × 4 = 34", "lt sm acc"))


def primes():
    out = []
    P = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
    for n in range(1, 31):
        r, c = divmod(n - 1, 10)
        x, y = 20 + c * 32, 30 + r * 42
        cls = "f1" if n in P else "f0"
        out.append(f'<rect class="{cls} st" x="{x}" y="{y}" width="30" height="36" rx="5"/>' + _t(x + 15, y + 24, str(n), "lt sm"))
    return _svg("".join(out) + _t(180, 180, "الأعداد الأوّليّة الأصغر من 30 ملوّنة", "lt sm") +
                _t(180, 208, "العدد الأوّليّ له قاسمان فقط: 1 ونفسه", "lt sm acc"))


def powers():
    out = []
    for i, n in enumerate((1, 2, 3)):
        x0 = 30 + i * 105
        s = 72 / n
        for r in range(n):
            for c in range(n):
                out.append(f'<rect class="f1 st" x="{x0 + c * s}" y="{40 + r * s}" width="{s}" height="{s}"/>')
        out.append(_t(x0 + 36, 140, f"{n}² = {n * n}", "lt acc"))
    return _svg("".join(out) + '<g class="lt" direction="ltr">' + _t(180, 178, "10³ = 10 × 10 × 10 = 1000", "lt") + "</g>" +
                _t(180, 206, "القوّة: ضرب العدد في نفسه عدّة مرّات", "lt sm"))


def lcm():
    out = ['<path class="ln" d="M20 70 H340 M20 150 H340"/>']
    for k in range(0, 13):
        x = 30 + k * 25
        out.append(f'<path class="ln" d="M{x} 64 V76 M{x} 144 V156"/>')
        if k % 4 == 0:
            out.append(f'<circle class="dot" cx="{x}" cy="70" r="7"/>')
        if k % 6 == 0:
            out.append(f'<circle class="dot" cx="{x}" cy="150" r="7"/>')
        out.append(_t(x, 176, str(k), "lt sm"))
    out.append('<path class="curve" stroke-dasharray="5 4" d="M330 60 V160"/>')
    return _svg("".join(out) + _t(180, 50, "ساعة A: كل 4 ساعات", "lt sm") + _t(180, 130, "ساعة B: كل 6 ساعات", "lt sm") +
                _t(180, 206, "ترنّان معًا بعد 12 ساعة = م.م.أ.ص(4؛6)", "lt sm acc"))


def irreducible():
    out = []
    for i, (n, k) in enumerate(((6, 4), (3, 2))):
        y = 50 + i * 70
        w = 240 / n
        for j in range(n):
            out.append(f'<rect class="{"f1" if j < k else "f0"} st" x="{60 + j * w}" y="{y}" width="{w}" height="40" rx="3"/>')
        out.append(_t(330, y + 27, f"{k}/{n}", "lt acc"))
    return _svg("".join(out) + _t(180, 190, "4/6 = 2/3 : نقسم البسط والمقام على 2", "lt sm") +
                _t(180, 212, "2/3 لا يمكن اختزاله أكثر", "lt sm acc"))


def dec_fractions():
    out = []
    for i in range(100):
        r, c = divmod(i, 10)
        out.append(f'<rect class="{"f1" if i < 37 else "f0"} st" x="{40 + c * 15}" y="{30 + r * 15}" width="15" height="15"/>')
    return _svg("".join(out) + '<g direction="ltr">' + _t(270, 90, "37/100", "lt big acc") + _t(270, 125, "= 0.37", "lt big") + "</g>" +
                _t(270, 160, "سبعة وثلاثون جزءًا من مئة", "lt sm"))


def dec_expand():
    heads = ["100", "10", "1", ",", "1/10", "1/100", "1/1000"]
    vals = ["", "3", "4", ",", "5", "4", "3"]
    out = []
    for i, (h, v) in enumerate(zip(heads, vals)):
        x = 20 + i * 47
        if h == ",":
            out.append(_t(x + 22, 100, ",", "lt big acc"))
            continue
        out.append(f'<rect class="{"f1" if i < 3 else "f2"} st" x="{x}" y="40" width="45" height="30" rx="4"/>' + _t(x + 22, 60, h, "lt sm"))
        out.append(f'<rect class="f0 st" x="{x}" y="76" width="45" height="36" rx="4"/>' + _t(x + 22, 101, v, "lt acc"))
    return _svg("".join(out) + '<g direction="ltr">' +
                _t(180, 150, "34.543 = 3×10 + 4 + 5×(1/10) + 4×(1/100) + 3×(1/1000)", "lt sm") + "</g>" +
                _t(180, 190, "الجزء الصحيح 34 والجزء العشريّ 0.543", "lt sm acc"))


def frac_mul():
    out = []
    for r in range(3):
        for c in range(4):
            cls = "f3" if (r < 2 and c < 3) else ("f1" if c < 3 else ("f2" if r < 2 else "f0"))
            out.append(f'<rect class="{cls} st" x="{50 + c * 45}" y="{30 + r * 45}" width="45" height="45"/>')
    return _svg("".join(out) + '<g direction="ltr">' + _t(300, 80, "3/4 × 2/3", "lt acc") + _t(300, 112, "= 6/12", "lt") +
                _t(300, 144, "= 1/2", "lt acc") + "</g>" + _t(180, 205, "الجزء المشترك يمثّل الجداء", "lt sm"))


def rationals():
    out = ['<path class="ln" d="M20 110 H340"/>']
    for k in range(-6, 7):
        x = 180 + k * 26
        out.append(f'<path class="ln" d="M{x} 104 V116"/>' + _t(x, 136, str(k).replace("-", "−"), "lt sm"))
    out.append('<rect class="f2 st" x="24" y="60" width="150" height="26" rx="6"/>' + _t(99, 78, "أعداد سالبة", "lt sm"))
    out.append('<rect class="f1 st" x="186" y="60" width="150" height="26" rx="6"/>' + _t(261, 78, "أعداد موجبة", "lt sm"))
    out.append('<circle class="dot" cx="102" cy="110" r="7"/><circle class="dot" cx="258" cy="110" r="7"/>')
    out.append('<path class="curve" d="M102 150 Q180 190 258 150"/>')
    return _svg("".join(out) + _t(180, 205, "−3 و+3 عددان متناظران: على البعد نفسه من الصفر", "lt sm acc"))


def compare():
    out = ['<rect class="f0 st" x="150" y="20" width="60" height="170" rx="30"/>',
           '<rect class="f3" x="166" y="120" width="28" height="62" rx="10"/>', '<circle class="f3" cx="180" cy="178" r="20"/>']
    for i, v in enumerate(range(20, -25, -5)):
        y = 36 + i * 15
        out.append(f'<path class="ln" d="M210 {y} H224"/>' + _t(246, y + 5, str(v).replace("-", "−"), "lt sm"))
    return _svg("".join(out) + _t(80, 70, "−5 < 0", "lt acc") + _t(80, 104, "−9 < −6", "lt acc") +
                _t(80, 140, "الأدنى هو الأصغر", "lt sm") + _t(300, 208, "ميزان الحرارة", "lt sm"))


def add_sub():
    out = ['<path class="ln" d="M20 130 H340"/>']
    for k in range(-6, 7):
        x = 180 + k * 26
        out.append(f'<path class="ln" d="M{x} 124 V136"/>' + _t(x, 156, str(k).replace("-", "−"), "lt sm"))
    out.append('<path class="curve" d="M50 124 Q115 50 180 124"/><path class="curve" d="M180 124 Q219 80 258 124"/>')
    out.append('<circle class="dot" cx="50" cy="130" r="7"/><circle class="dot" cx="258" cy="130" r="7"/>')
    return _svg("".join(out) + _t(115, 70, "+5", "lt acc") + _t(219, 86, "+3", "lt acc") +
                _t(180, 196, "(−5) + (+5) + (+3) = +3", "lt sm acc"))


def lines_circles():
    return _svg('''<circle class="f1 st2" cx="120" cy="110" r="70"/>
  <path class="ln" d="M120 110 L185 84"/><path class="ln" d="M50 110 H190"/><path class="line2" d="M20 190 H340"/>
  <path class="line2" d="M240 20 V200 M290 20 V200"/>
  <circle class="dot" cx="120" cy="110" r="5"/>''' + _t(112, 104, "O", "lt sm") + _t(162, 88, "r", "lt sm acc") +
                _t(80, 128, "قطر", "lt sm") + _t(265, 110, "∥", "lt big acc") + _t(300, 184, "مماسّ", "lt sm"))


def angles():
    return _svg('''<path class="ln" d="M40 170 H320"/><path class="ln" d="M180 170 L90 40"/><path class="line2" d="M180 170 L300 60"/>
  <path class="curve" d="M140 170 A40 40 0 0 1 157 137"/><path class="curve" d="M220 170 A40 40 0 0 0 209 142"/>
  <circle class="dot" cx="180" cy="170" r="5"/>''' + _t(128, 150, "125°", "lt sm acc") + _t(236, 150, "40°", "lt sm acc") +
                _t(180, 205, "زاويتان متجاورتان: رأس مشترك وضلع مشترك", "lt sm"))


def triangles():
    return _svg('''<path class="f1 st2" d="M20 170 L110 170 L65 92 Z"/><path class="f2 st2" d="M135 170 L225 170 L180 60 Z"/>
  <path class="f3 st2" d="M250 170 L340 170 L250 90 Z"/><path class="ln" d="M250 158 h12 v12"/>''' +
                _t(65, 195, "متساوي الأضلاع", "lt xs") + _t(180, 195, "متساوي الساقين", "lt xs") + _t(295, 195, "قائم الزاوية", "lt xs") +
                _t(180, 30, "مجموع زوايا المثلّث 180°", "lt sm acc"))


def areas():
    out = []
    for r in range(4):
        for c in range(6):
            out.append(f'<rect class="f1 st" x="{30 + c * 26}" y="{40 + r * 26}" width="26" height="26"/>')
    return _svg("".join(out) + '''<path class="f2 st2" d="M220 144 L340 144 L260 40 Z"/><path class="ln" stroke-dasharray="5 4" d="M260 40 V144"/>''' +
                _t(108, 170, "6 × 4 = 24 وحدة مساحة", "lt sm acc") + _t(280, 170, "(قاعدة × ارتفاع) ÷ 2", "lt sm acc") +
                _t(180, 205, "المساحة: عدد المربّعات التي تغطّي الشكل", "lt sm"))


def ratio():
    out = []
    for i in range(3):
        out.append(f'<circle class="f2 st" cx="{60 + i * 40}" cy="80" r="16"/>')
    for i in range(2):
        out.append(f'<rect class="f1 st" x="{50 + i * 40}" y="120" width="30" height="30" rx="5"/>')
    return _svg("".join(out) + _t(250, 90, "3 أكواب طحين", "lt sm") + _t(250, 140, "2 كوب حليب", "lt sm") +
                _t(180, 190, "3 : 2 = 3/2", "lt big acc") + _t(180, 214, "نسبة الطحين إلى الحليب", "lt sm"))


def literal():
    return _svg('''<rect class="f1 st" x="40" y="50" width="80" height="60" rx="8"/><rect class="f1 st" x="140" y="50" width="80" height="60" rx="8"/>
  <rect class="f2 st" x="240" y="50" width="80" height="60" rx="8"/>''' + _t(80, 87, "x", "lt big acc") + _t(180, 87, "x", "lt big acc") +
                _t(280, 87, "3", "lt big") + _t(130, 86, "+", "lt") + _t(230, 86, "+", "lt") +
                _t(180, 150, "2x + 3", "lt big acc") + _t(180, 190, "الحرف يحلّ محلّ عدد مجهول", "lt sm"))


def percent():
    out = []
    for i in range(100):
        r, c = divmod(i, 10)
        out.append(f'<rect class="{"f1" if i < 25 else "f0"} st" x="{30 + c * 15}" y="{30 + r * 15}" width="15" height="15"/>')
    return _svg("".join(out) + _t(265, 90, "25%", "lt big acc") + _t(265, 125, "= 25/100 = 1/4", "lt") +
                _t(265, 160, "25 من كلّ 100", "lt sm"))


def proportional():
    rows = [("كيلو بندورة", ["1", "2", "4", "6"]), ("السعر (ألف ل.ل)", ["25", "50", "100", "150"])]
    out = []
    for r, (h, vals) in enumerate(rows):
        y = 50 + r * 44
        out.append(f'<rect class="f2 st" x="230" y="{y}" width="110" height="40" rx="4"/>' + _t(285, y + 26, h, "lt xs"))
        for i, v in enumerate(vals):
            out.append(f'<rect class="f1 st" x="{20 + i * 52}" y="{y}" width="50" height="40" rx="4"/>' + _t(45 + i * 52, y + 26, v))
    out.append('<path class="curve" d="M40 140 Q30 160 60 170"/>')
    return _svg("".join(out) + _t(160, 175, "× 25", "lt acc") + _t(180, 208, "معامل التناسب 25", "lt sm"))


def stats():
    vals = [5, 8, 6, 9, 4]
    out = ['<path class="ln" d="M40 170 H330 M40 170 V30"/>']
    for i, v in enumerate(vals):
        x = 60 + i * 54
        out.append(f'<rect class="{"f1" if i % 2 == 0 else "f2"} st" x="{x}" y="{170 - v * 15}" width="36" height="{v * 15}" rx="3"/>' +
                   _t(x + 18, 164 - v * 15, str(v), "lt sm"))
    days = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"]
    for i, d in enumerate(days):
        out.append(_t(78 + i * 54, 190, d, "lt xs"))
    return _svg("".join(out) + _t(185, 214, "عدد الكتب المستعارة من المكتبة", "lt sm acc"))


FIGS = {
    "naturals": (naturals, "لوحة المنازل: كل حلقة من ثلاثة أرقام"),
    "order": (order, "سلّم الأولويّات: من الأعلى إلى الأسفل"),
    "primes": (primes, "غربال الأعداد الأوّليّة"),
    "powers": (powers, "المربّع: عدد مضروب في نفسه"),
    "lcm": (lcm, "ساعتان ترنّان: متى ترنّان معًا؟"),
    "irreducible": (irreducible, "كسران متساويان: الشكل نفسه بقطع أقلّ"),
    "dec-fractions": (dec_fractions, "مربّع المئة: 37 مربّعًا ملوّنًا من 100"),
    "dec-expand": (dec_expand, "جدول المنازل للعدد العشريّ 34.543"),
    "frac-mul": (frac_mul, "نموذج المساحة لضرب كسرين"),
    "rationals": (rationals, "المحور العدديّ: السالب يسار الصفر والموجب يمينه"),
    "compare": (compare, "ميزان الحرارة يقارن الأعداد النسبيّة"),
    "add-sub": (add_sub, "الجمع على المحور: قفزات إلى اليمين"),
    "lines-circles": (lines_circles, "الدائرة وعناصرها، ومستقيمان متوازيان"),
    "angles": (angles, "الزوايا حول نقطة على مستقيم"),
    "triangles": (triangles, "أنواع المثلّثات"),
    "areas": (areas, "مساحة المستطيل والمثلّث"),
    "ratio": (ratio, "النسبة في الوصفة"),
    "literal": (literal, "العبارة الحرفيّة 2x + 3"),
    "percent": (percent, "النسبة المئويّة: من كل 100"),
    "proportional": (proportional, "جدول تناسب: ثمن البندورة"),
    "stats": (stats, "تمثيل بيانيّ بالأعمدة"),
}
