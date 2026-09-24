# -*- coding: utf-8 -*-
"""Hand-built SVG illustrations for the grade-7 lessons. Colours come from CSS classes (theme-aware)."""


def _svg(body, vb="0 0 360 220"):
    return f'<svg class="il" viewBox="{vb}" role="img" aria-hidden="true">{body}</svg>'


def powers():
    cells, v = [], 1
    for r in range(2):
        for c in range(4):
            x, y = 30 + c * 48, 40 + r * 48
            cells.append(f'<rect class="{"f1" if (r + c) % 2 == 0 else "f2"} st" x="{x}" y="{y}" width="48" height="48"/>'
                         f'<text x="{x + 24}" y="{y + 30}" text-anchor="middle" class="lt">{v}</text>')
            v *= 2
    return _svg("".join(cells) + '''
  <g class="lt" direction="ltr"><text x="238" y="72">× 2 × 2 × 2 …</text><text x="238" y="104" class="acc">square n → 2ⁿ⁻¹</text>
  <text x="238" y="136" class="sm">2⁷ = 128</text></g>
  <text x="126" y="170" text-anchor="middle" class="lt sm">رقعة الشطرنج: الحبّات تتضاعف</text>''')


def primes():
    return _svg('''
  <path class="ln" d="M110 42 L80 78 M110 42 L140 78 M140 96 L112 132 M140 96 L168 132 M168 150 L142 186 M168 150 L194 186"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="110" y="36" class="big">84</text>
    <circle class="f1" cx="80" cy="88" r="14"/><text x="80" y="94" class="acc">2</text><text x="140" y="92">42</text>
    <circle class="f1" cx="112" cy="142" r="14"/><text x="112" y="148" class="acc">2</text><text x="168" y="146">21</text>
    <circle class="f1" cx="142" cy="196" r="14"/><text x="142" y="202" class="acc">3</text>
    <circle class="f1" cx="194" cy="196" r="14"/><text x="194" y="202" class="acc">7</text>
  </g>
  <g class="lt" direction="ltr"><text x="232" y="100" class="big">84 = 2² × 3 × 7</text><text x="232" y="130" class="sm">GCD · LCM</text></g>''')


def fractions():
    top = "".join(f'<rect class="{"f1" if i < 6 else "card"} st2" x="{30 + i * 30}" y="40" width="30" height="40"/>' for i in range(8))
    bot = "".join(f'<rect class="{"f2" if i < 3 else "card"} st2" x="{30 + i * 60}" y="110" width="60" height="40"/>' for i in range(4))
    return _svg(top + bot + '''
  <g class="lt" direction="ltr"><text x="284" y="66" class="big">6/8</text><text x="284" y="136" class="big">3/4</text>
  <text x="284" y="102" class="acc">=</text></g>
  <text x="150" y="186" text-anchor="middle" class="lt sm">الشريطان متساويان في الطول الملوّن: الاختزال لا يغيّر القيمة</text>''')


def decimals():
    X = lambda v: 30 + v * 300
    ticks = "".join(f'<path class="ax" d="M{X(i / 10):.0f} {104 if i % 5 else 98} V{116 if i % 5 else 122}"/>' for i in range(11))
    pts = [(0.25, "1/4 = 0.25", 70), (0.375, "3/8 = 0.375", 46), (2 / 3, "2/3 ≈ 0.667", 70)]
    marks = "".join(f'<circle class="dot" cx="{X(v):.1f}" cy="110" r="6"/><text x="{X(v):.1f}" y="{y}" text-anchor="middle" class="lt sm" direction="ltr">{t}</text>'
                    for v, t, y in pts)
    return _svg(f'''<path class="ax" d="M30 110 H330"/>{ticks}{marks}
  <g class="lt sm" text-anchor="middle" direction="ltr"><text x="30" y="142">0</text><text x="180" y="142">0.5</text><text x="330" y="142">1</text></g>
  <text x="180" y="182" text-anchor="middle" class="lt sm">مقام من العوامل 2 و5 فقط ← عدد عشريّ منتهٍ</text>''')


def signed_add():
    X = lambda v: 180 + v * 24
    ticks = "".join(f'<path class="ax" d="M{X(i)} 132 V144"/><text x="{X(i)}" y="164" text-anchor="middle" class="lt sm" direction="ltr">{i}</text>' for i in range(-6, 7, 2))
    return _svg(f'''<path class="ax" d="M20 138 H340"/>{ticks}
  <path class="curve" d="M{X(-5)} 132 Q {X(-1)} 40 {X(3)} 132"/><path class="arrow" d="M{X(3) - 10} 122 L{X(3)} 132 L{X(3) + 4} 118"/>
  <circle class="dot" cx="{X(-5)}" cy="138" r="6"/><circle class="dot" cx="{X(3)}" cy="138" r="6"/>
  <text x="{X(-1)}" y="70" text-anchor="middle" class="lt acc" direction="ltr">+8</text>
  <text x="180" y="200" text-anchor="middle" class="lt" direction="ltr">(−5) + (+8) = +3</text>''')


def signed_mul():
    cell = lambda x, y, s, cls: f'<rect class="{cls} st" x="{x}" y="{y}" width="60" height="50" rx="6"/><text x="{x + 30}" y="{y + 34}" text-anchor="middle" class="lt big">{s}</text>'
    return _svg(f'''
  <g class="lt" text-anchor="middle" direction="ltr"><text x="130" y="36">+</text><text x="190" y="36">−</text><text x="80" y="80">+</text><text x="80" y="130">−</text>
  <text x="80" y="36" class="sm">×</text></g>
  {cell(100, 46, "+", "f1")}{cell(160, 46, "−", "f3")}{cell(100, 96, "−", "f3")}{cell(160, 96, "+", "f1")}
  <g class="lt sm" direction="ltr"><text x="246" y="76">(−5) × (−4) = +20</text><text x="246" y="104">(+5) × (−6) = −30</text><text x="246" y="132">(−24) ÷ (+6) = −4</text></g>
  <text x="180" y="186" text-anchor="middle" class="lt sm">إشارتان متماثلتان ← موجب · مختلفتان ← سالب</text>''')


def plane():
    ox, oy, s = 180, 110, 18
    grid = "".join(f'<path class="grid" d="M{ox + i * s} {oy - 5 * s} V{oy + 5 * s} M{ox - 7 * s} {oy + i * s} H{ox + 7 * s}"/>' for i in range(-5, 6))
    grid += "".join(f'<path class="grid" d="M{ox + i * s} {oy - 5 * s} V{oy + 5 * s}"/>' for i in (-7, -6, 6, 7))
    pts = [("A", 2, 3), ("B", -3, 4), ("C", -4, -2), ("D", 5, -1)]
    dots = "".join(f'<circle class="dot" cx="{ox + a * s}" cy="{oy - b * s}" r="5"/><text x="{ox + a * s + 7}" y="{oy - b * s - 6}" class="lt sm" direction="ltr">{n}({a};{b})</text>'
                   for n, a, b in pts)
    return _svg(f'''{grid}<path class="ax" d="M{ox - 7 * s} {oy} H{ox + 7 * s} M{ox} {oy - 5 * s} V{oy + 5 * s}"/>{dots}
  <g class="lt acc" text-anchor="middle"><text x="{ox + 4 * s}" y="{oy - 3 * s}">I</text><text x="{ox - 5 * s}" y="{oy - 1 * s}">II</text>
  <text x="{ox - 2 * s}" y="{oy + 4 * s}">III</text><text x="{ox + 3 * s}" y="{oy + 4 * s}">IV</text></g>''')


def algebra():
    return _svg('''
  <rect class="f1 st" x="40" y="60" width="150" height="70"/><rect class="f2 st" x="190" y="60" width="70" height="70"/>
  <g class="lt" text-anchor="middle" direction="ltr"><text x="115" y="102" class="big">2x</text><text x="225" y="102" class="big">6</text>
  <text x="115" y="50" class="sm">x</text><text x="225" y="50" class="sm">3</text><text x="26" y="100" class="sm">2</text></g>
  <text x="150" y="170" text-anchor="middle" class="lt acc" direction="ltr">2(x + 3) = 2x + 6</text>
  <text x="150" y="196" text-anchor="middle" class="lt sm">التوسيع ← ← التحليل</text>''')


def equations():
    boxes = "".join(f'<rect class="f1 st" x="{48 + i * 30}" y="82" width="26" height="26" rx="4"/><text x="{61 + i * 30}" y="100" text-anchor="middle" class="lt sm" direction="ltr">x</text>' for i in range(3))
    return _svg(f'''
  <path class="ln" d="M180 60 V170 M140 170 H220"/><path class="ln" d="M40 110 H320"/>
  <path class="ln" d="M40 110 L60 60 M100 110 L80 60"/><path class="ln" d="M260 110 L280 60 M320 110 L300 60"/>
  {boxes}<rect class="f2 st" x="140" y="82" width="30" height="26" rx="4"/><text x="155" y="100" text-anchor="middle" class="lt sm">5</text>
  <rect class="f2 st" x="262" y="78" width="56" height="30" rx="4"/><text x="290" y="99" text-anchor="middle" class="lt">14</text>
  <circle class="dot" cx="180" cy="60" r="6"/>
  <text x="180" y="200" text-anchor="middle" class="lt acc" direction="ltr">3x + 5 = 14  →  x = 3</text>''')


def proportion():
    ox, oy, s = 50, 180, 24
    grid = "".join(f'<path class="grid" d="M{ox + i * s} {oy} V{oy - 6 * s} M{ox} {oy - i * s} H{ox + 5 * s}"/>' for i in range(7))
    dots = "".join(f'<circle class="dot" cx="{ox + k * s}" cy="{oy - 2 * k * s / 2}" r="5"/>' for k in (1, 2, 3))
    return _svg(f'''{grid}<path class="ax" d="M{ox} {oy} H{ox + 5 * s + 6} M{ox} {oy} V{oy - 6 * s - 6}"/>
  <path class="curve" d="M{ox} {oy} L{ox + 5 * s} {oy - 5 * s}"/>{dots}
  <g class="lt" direction="ltr"><text x="210" y="70" class="acc">y = 2x ?</text></g>
  <g class="lt sm" direction="ltr"><text x="210" y="100">kg:  1   2   3</text><text x="210" y="124">$:   2   4   6</text></g>
  <text x="250" y="160" text-anchor="middle" class="lt sm">مستقيم يمرّ بالأصل ← تناسب</text>''')


def triangles():
    return _svg('''
  <path class="f1 st2" d="M30 170 L150 170 L70 60 Z"/><path class="f1 st2" d="M200 170 L320 170 L240 60 Z"/>
  <path class="ln" d="M86 166 V174 M90 166 V174 M256 166 V174 M260 166 V174"/>
  <path class="ln" d="M44 112 l8 4 M214 112 l8 4"/>
  <path class="curve" d="M52 170 A 22 22 0 0 0 43 152"/><path class="curve" d="M222 170 A 22 22 0 0 0 213 152"/>
  <g class="lt" text-anchor="middle" direction="ltr"><text x="30" y="190">A</text><text x="150" y="190">B</text><text x="70" y="52">C</text>
  <text x="200" y="190">D</text><text x="320" y="190">E</text><text x="240" y="52">F</text></g>
  <text x="180" y="212" text-anchor="middle" class="lt acc">C-A-C</text>''')


def angles():
    return _svg('''
  <path class="line1" d="M20 70 H340"/><path class="line1" d="M20 150 H340"/><path class="line2" d="M110 200 L250 20"/>
  <path class="curve" d="M218 70 A 24 24 0 0 0 204 51"/><path class="curve" d="M142 150 A 24 24 0 0 1 156 169"/>
  <g class="lt" direction="ltr"><text x="222" y="62" class="acc">65°</text><text x="112" y="180" class="acc">65°</text>
  <text x="172" y="92" class="sm">115°</text><text x="300" y="62" class="sm l1">(d₁)</text><text x="300" y="142" class="sm l1">(d₂)</text></g>
  <text x="180" y="212" text-anchor="middle" class="lt sm">مستقيمان متوازيان وقاطع: المتبادلتان داخليًّا متساويتان</text>''')


def bisectors():
    return _svg('''
  <path class="ln" d="M60 140 H300"/><path class="line2" stroke-dasharray="6 5" d="M180 20 V200"/>
  <path class="arrow" d="M180 88 L60 140 M180 88 L300 140"/>
  <circle class="dot" cx="60" cy="140" r="6"/><circle class="dot" cx="300" cy="140" r="6"/><circle class="dot" cx="180" cy="88" r="7"/>
  <path class="ln" d="M172 140 v-8 h8"/>
  <g class="lt" direction="ltr"><text x="44" y="162">A</text><text x="306" y="162">B</text><text x="188" y="80" class="acc">C</text>
  <text x="104" y="104" class="sm">25 m</text><text x="236" y="104" class="sm">25 m</text></g>
  <text x="180" y="214" text-anchor="middle" class="lt sm">الجائزة على المنصّف العموديّ ← اللعبة عادلة (CA = CB)</text>''')


FIGS = {
    "powers": (powers, "القوّة تكرار للضرب: كل مربّع ضعف السابق"),
    "primes": (primes, "شجرة العوامل: كل عدد جداء أعداد أوّليّة"),
    "fractions": (fractions, "\\(\\frac68=\\frac34\\): كسران متساويان بكتابتين"),
    "decimals": (decimals, "الكسور على المستقيم العدديّ بين 0 و1"),
    "signed_add": (signed_add, "الجمع على المستقيم العدديّ: نبدأ من −5 ونقفز 8 إلى اليمين"),
    "signed_mul": (signed_mul, "جدول قاعدة الإشارات"),
    "plane": (plane, "المَعلَم وأرباعه الأربعة (من ورقة العمل)"),
    "algebra": (algebra, "نموذج المساحة: التوسيع والتحليل وجهان لعمليّة واحدة"),
    "equations": (equations, "المعادلة ميزان متوازن (نشاط الميزان في الخطّة)"),
    "proportion": (proportion, "التناسب: النقاط على مستقيم يمرّ بالأصل"),
    "triangles": (triangles, "مثلّثان متساويان: ضلعان والزاوية المحصورة (C-A-C)"),
    "angles": (angles, "الزوايا عند مستقيمين متوازيين وقاطع"),
    "bisectors": (bisectors, "«لمن السبق اليوم؟»: نقطة على المنصّف العموديّ تبعد البعد نفسه عن A وB"),
}
