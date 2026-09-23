# -*- coding: utf-8 -*-
"""Hand-built SVG illustrations, one per lesson. Colors come from CSS classes (theme-aware)."""


def _svg(body, vb="0 0 360 220"):
    return f'<svg class="il" viewBox="{vb}" role="img" aria-hidden="true">{body}</svg>'


def expand():
    return _svg('''
  <rect class="f1 st" x="40" y="30" width="100" height="100"/>
  <rect class="f2 st" x="140" y="30" width="60" height="100"/>
  <rect class="f2 st" x="40" y="130" width="100" height="60"/>
  <rect class="f3 st" x="140" y="130" width="60" height="60"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="90" y="86" class="big">a²</text><text x="170" y="86">ab</text>
    <text x="90" y="166">ab</text><text x="170" y="166">b²</text>
    <text x="90" y="22" class="sm">a</text><text x="170" y="22" class="sm">b</text>
    <text x="28" y="86" class="sm">a</text><text x="28" y="166" class="sm">b</text>
  </g>
  <g class="lt" direction="ltr"><text x="218" y="98">(a + b)² =</text><text x="218" y="126" class="acc">a² + 2ab + b²</text></g>''')


def factor():
    return _svg('''
  <rect class="f1 st" x="40" y="40" width="110" height="110"/>
  <rect class="f2 st" x="150" y="40" width="70" height="110"/>
  <path class="ln" d="M40 165 v8 h180 v-8 M130 173 v6"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="95" y="102" class="big">x²</text><text x="185" y="102" class="big">7x</text>
    <text x="130" y="198" class="sm">x + 7</text><text x="26" y="100" class="sm">x</text>
  </g>
  <g class="lt" direction="ltr"><text x="238" y="92">x² + 7x</text><text x="238" y="122" class="acc">= x (x + 7)</text></g>''')


def poly():
    pts = []
    for i in range(0, 55):
        X = 139 + i * 3
        Y = 150 - (100 / 4900) * (X - 150) * (290 - X)
        pts.append(f"{X},{Y:.1f}")
    return _svg(f'''
  <path class="ax" d="M20 150 H345 M110 205 V15"/>
  <polyline class="curve" points="{' '.join(pts)}"/>
  <circle class="dot" cx="150" cy="150" r="5"/><circle class="dot" cx="290" cy="150" r="5"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="150" y="176" class="sm">x₁</text><text x="290" y="176" class="sm">x₂</text>
    <text x="220" y="40" class="acc">P(x)</text>
  </g>
  <text x="220" y="112" text-anchor="middle" class="lt sm">ربح</text>
  <text x="100" y="40" text-anchor="end" class="lt sm">نقطتا التعادل:</text><text x="100" y="60" text-anchor="end" class="lt sm" direction="ltr">P(x) = 0</text>''')


def roots():
    return _svg('''
  <rect class="tray" x="55" y="25" width="160" height="160" rx="10"/>
  <rect class="f1" x="65" y="35" width="140" height="140" rx="4"/>
  <g transform="rotate(-45 135 105)">
    <rect class="bread" x="52" y="92" width="166" height="26" rx="13"/>
    <path class="score" d="M85 98 l10 14 M115 98 l10 14 M145 98 l10 14 M175 98 l10 14"/>
  </g>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="135" y="205" class="sm">30 cm</text><text x="36" y="110" class="sm">30</text>
  </g>
  <g class="lt" direction="ltr"><text x="232" y="92" class="acc">30√2 cm</text><text x="232" y="118" class="sm">≈ 42.4 cm &gt; 40 cm</text></g>''')


def rational():
    x707 = 40 + 0.7071 * 280
    return _svg(f'''
  <rect class="card" x="48" y="22" width="90" height="82" rx="10"/>
  <rect class="card acc-card" x="222" y="22" width="90" height="82" rx="10"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="93" y="56" class="big">1</text><path class="ln" d="M70 66 H116"/><text x="93" y="92" class="big">√2</text>
    <text x="267" y="56" class="big">√2</text><path class="ln" d="M244 66 H290"/><text x="267" y="92" class="big">2</text>
    <text x="180" y="58" class="sm">× √2 / √2</text>
  </g>
  <path class="arrow" d="M150 68 H208 m-8 -6 l8 6 l-8 6"/>
  <path class="ax" d="M40 160 H320 M40 152 v16 M180 154 v12 M320 152 v16"/>
  <circle class="dot" cx="{x707:.1f}" cy="160" r="6"/>
  <g class="lt" text-anchor="middle" direction="ltr">
    <text x="40" y="190" class="sm">0</text><text x="180" y="190" class="sm">0.5</text><text x="320" y="190" class="sm">1</text>
    <text x="{x707:.1f}" y="140" class="acc">≈ 0.707</text>
  </g>''')


def systems():
    ox, oy, s = 50, 190, 30
    grid = "".join(f'<path class="grid" d="M{ox + i*s} {oy} V{oy - 5*s} M{ox} {oy - i*s} H{ox + 6*s}"/>' for i in range(0, 7))
    return _svg(f'''
  {grid}
  <path class="ax" d="M{ox} {oy} H{ox + 6*s + 6} M{ox} {oy} V{oy - 5*s - 6}"/>
  <path class="line1" d="M{ox} {oy - 4.5*s} L{ox + 3*s} {oy}"/>
  <path class="line2" d="M{ox} {oy - 2.833*s:.1f} L{ox + 4.25*s:.1f} {oy}"/>
  <circle class="dot" cx="{ox + 2*s}" cy="{oy - 1.5*s}" r="6"/>
  <g class="lt" direction="ltr">
    <text x="{ox + 2*s + 10}" y="{oy - 1.5*s - 10}" class="acc">(2 ; 1.5)</text>
    <text x="{ox + 8}" y="{oy - 4.5*s + 4}" class="sm l1">3x + 2y = 9</text>
    <text x="{ox + 3.3*s:.0f}" y="{oy - 1.0*s:.0f}" class="sm l2">2x + 3y = 8.5</text>
  </g>
  <g class="lt" text-anchor="middle"><text x="300" y="70" class="sm">منقوشة: 2 دولار</text><text x="300" y="96" class="sm">عصير: 1.5 دولار</text></g>''')


FIGS = {
    "expand": (expand, "النموذج الهندسيّ: مساحة المربّع الكبير = مجموع مساحات الأجزاء الأربعة"),
    "factor": (factor, "التحليل يعيد المستطيلات إلى مستطيل واحد: الطول × العرض"),
    "poly": (poly, "منحنى ربح مطعم: الشكل المحلَّل يعطي فورًا نقطتَي التعادل"),
    "roots": (roots, "هل تتّسع باغيت طولها 40 cm على قطر صينيّة ضلعها 30 cm؟"),
    "rational": (rational, "العدد نفسه بكتابتين: الثانية أسهل في الحساب والمقارنة"),
    "systems": (systems, "حلّ النظام هو نقطة تقاطع المستقيمين: مسألة المناقيش والعصير"),
}
