# -*- coding: utf-8 -*-
"""كتاب التمارين — a separate exercises-only workbook for grade 6 (21 worksheets + answer key).

Every exercise is generated from a small template with fixed random seeds; the answer is computed
in Python at the same time, so the answer key is correct by construction.
python3 workbook.py  →  كتاب-التمارين-الصف-السادس.pdf  +  حلول-كتاب-التمارين-الصف-السادس.pdf
"""
import math, os, random, re
from fractions import Fraction as F

import build, make_pdf
from content import LESSONS, UNITS

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK, KEY = "كتاب-التمارين-الصف-السادس.pdf", "حلول-كتاب-التمارين-الصف-السادس.pdf"


# ---------------------------------------------------------------- formatting helpers
def g(n):
    """Integer with thin-space thousands groups (for TeX)."""
    s = f"{abs(int(n)):,}".replace(",", r"\,")
    return ("-" if n < 0 else "") + s


def fr(x):
    x = F(x)
    if x.denominator == 1:
        return g(x.numerator)
    sgn = "-" if x < 0 else ""
    return rf"{sgn}\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def dec(x, nd=None):
    x = F(x)
    s = f"{float(x):.{nd}f}" if nd is not None else (str(float(x)).rstrip("0").rstrip(".") if x.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100, 125, 200, 250, 500, 1000) else str(float(x)))
    return s


def M(t):
    return rf"\({t}\)"


def rnd(x, step=1):
    """School rounding (half up) of x to a multiple of step."""
    return int(math.floor(F(x) / step + F(1, 2))) * step


TIMES, DEG, SQ = r"\times", r"^\circ", r"\square"


def deg(a):
    return M(f"{a}" + DEG)


def frc(a, b):
    return M(r"\frac{%s}{%s}" % (a, b))


def hat(name):
    return r"\widehat{%s}" % name


def sg(n):
    return f"+{n}" if n > 0 else str(n)


# ---------------------------------------------------------------- per-lesson generators
# each returns dict(drill=[(q, a)], varied=[(q, a)], problems=[(q, a)])

def w_naturals(r):
    drill = []
    for _ in range(4):
        d = [r.randint(1, 9), r.randint(0, 9), r.randint(0, 9), r.randint(1, 9)]
        e = sorted(r.sample(range(0, 9), 4), reverse=True)
        n = sum(a * 10 ** k for a, k in zip(d, e))
        drill.append((M("+".join(rf"{a}\times10^{{{k}}}" if k > 1 else (rf"{a}\times10" if k == 1 else str(a)) for a, k in zip(d, e)) + r"=\ ?"), M(g(n))))
    for _ in range(4):
        n = r.randint(1_000_000, 99_999_999)
        drill.append((f"قرّب {M(g(n))} إلى أقرب ألف.", M(g(rnd(n, 1000)))))
    nums = r.sample(range(100_000, 9_999_999), 4)
    n = r.randint(10_000_000, 999_999_999)
    varied = [(f"رتّب تصاعديًّا: {'؛ '.join(M(g(x)) for x in nums)}", M(r"<".join(g(x) for x in sorted(nums)))),
              (f"في العدد {M(g(n))}: ما رقم الآلاف؟ وما عدد الآلاف؟", f"رقم الآلاف {(n // 1000) % 10}؛ عدد الآلاف {M(g(n // 1000))}"),
              (f"اكتب العدد الموجود في لوحة المنازل، ثم اكتبه بالحروف. [[fig:pv|{n}]]", M(g(n))),
              (f"أيّهما أكبر: {M(g(nums[0]))} أم {M(g(nums[1]))}؟ علّل.", M(g(max(nums[:2]))))]
    a, b, c = r.randint(1_000, 9_000) * 1000, r.randint(100, 900) * 1000, r.randint(10, 90) * 1000
    pop = r.randint(1_200_000, 4_900_000)
    problems = [(f"جمعت مدرسة {M(g(a))} ليرة ثم {M(g(b))} ليرة ثم {M(g(c))} ليرة. ما المبلغ الكلّي؟", M(g(a + b + c)) + " ليرة"),
                (f"عدد سكّان مدينة {M(g(pop))} نسمة. قرّبه إلى أقرب مئة ألف ثم إلى أقرب مليون.", f"{M(g(rnd(pop, 100000)))}؛ {M(g(rnd(pop, 1000000)))}"),
                ("اكتب أكبر عدد وأصغر عدد من سبعة أرقام مختلفة.", M(r"9\,876\,543") + " و" + M(r"1\,023\,456"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_order(r):
    drill = []
    for _ in range(8):
        a, b, c, d = (r.randint(2, 12) for _ in range(4))
        form = r.randint(0, 3)
        if form == 0:
            t, v = rf"{a}+{b}\times{c}", a + b * c
        elif form == 1:
            t, v = rf"({a}+{b})\times{c}", (a + b) * c
        elif form == 2:
            t, v = rf"{a * c}\div{c}+{b}\times{d}", a + b * d
        else:
            t, v = rf"{a}\times({b + c}-{c})+{d}", a * b + d
        drill.append((M(t), M(v)))
    a, b, c, d = r.randint(3, 9), r.randint(2, 9), r.randint(2, 9), r.randint(1, 5)
    varied = [(f"ضع أقواسًا لتصبح المساواة صحيحة: {M(str(a) + TIMES + f'{b}+{c}-{d}={a * (b + c) - d}')}", M(rf"{a}\times({b}+{c})-{d}")),
              (f"ضع أقواسًا لتصبح المساواة صحيحة: {M(str(a) + TIMES + f'{b}+{c}-{d}={a * (b + c - d)}')}", M(rf"{a}\times({b}+{c}-{d})")),
              (f"احسب بطريقتين (بالتوزيع): {M(str(a) + TIMES + f'({b * 10}+{c})')}", M(rf"{a}\times{b * 10}+{a}\times{c}={a * (b * 10 + c)}")),
              (f"صح أم خطأ؟ صحّح إن لزم: {M(f'{a + b}-{b}' + TIMES + f'{c}={a * c}')}", f"خطأ: {M(a + b - b * c)}" if a + b - b * c != a * c else "صحيح")]
    p1, n1, p2, n2 = r.randint(2, 9) * 500, r.randint(2, 6), r.randint(2, 9) * 250, r.randint(2, 6)
    paid = (p1 * n1 + p2 * n2) // 10000 * 10000 + 10000
    problems = [(f"اشترت ريم {n1} دفاتر بـ {M(g(p1))} ليرة للدفتر و{n2} أقلام بـ {M(g(p2))} ليرة للقلم، ودفعت {M(g(paid))} ليرة. اكتب عبارة واحدة للباقي واحسبه.",
                 M(rf"{g(paid)}-({n1}\times{g(p1)}+{n2}\times{g(p2)})={g(paid - p1 * n1 - p2 * n2)}")),
                (f"في الصفّ {a} صفوف في كلّ منها {b} مقاعد، وغاب {d} طلّاب. كم طالبًا حضر إذا كانت كل المقاعد مشغولة عادةً؟", M(rf"{a}\times{b}-{d}={a * b - d}")),
                (f"اشترى أب {c} علب في كلّ منها {b * 2} قلمًا، ثم اشترى {d} أقلام. اكتب عبارة واحدة واحسب.", M(rf"{c}\times{b * 2}+{d}={c * b * 2 + d}"))]
    return dict(drill=drill, varied=varied, problems=problems)


def _factor(n):
    f, p = {}, 2
    while n > 1:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    return f


def _ftex(f):
    return r"\times".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in sorted(f.items()))


def w_primes(r):
    pool = [n for n in range(24, 400) if len(_factor(n)) >= 2 and max(_factor(n)) < 12]
    nums = r.sample(pool, 8)
    drill = [(f"حلّل إلى عوامل أوّليّة: {M(n)}", M(f"{n}={_ftex(_factor(n))}")) for n in nums[:6]]
    cand = r.sample(range(11, 60), 8)
    pr = [x for x in cand if len(_factor(x)) == 1 and list(_factor(x).values())[0] == 1]
    drill.append((f"حدّد الأعداد الأوّليّة: {'، '.join(map(str, cand))}", "، ".join(map(str, pr)) or "لا يوجد"))
    n = r.randint(100, 999) * 9 + r.randint(0, 8)
    drill.append((f"هل يقبل {M(n)} القسمة على 3؟ على 9؟ (استعمل مجموع الأرقام)", f"مجموع الأرقام {sum(map(int, str(n)))}: على 3 {'نعم' if n % 3 == 0 else 'لا'}، على 9 {'نعم' if n % 9 == 0 else 'لا'}"))
    k = r.choice([48, 60, 72, 84, 90])
    varied = [(f"أكمل شجرة العوامل ثم اكتب التحليل. [[fig:ftree|{k}]]", M(f"{k}={_ftex(_factor(k))}")),
              (f"اكتب كلّ قواسم {M(k)}.", "، ".join(str(d) for d in range(1, k + 1) if k % d == 0)),
              ("أكمل الرقم الناقص ليقبل العدد القسمة على 9: " + M(r"5\square4"), M("0") + " أو " + M("9")),
              ("اكتشف الخطأ: «كل عدد فرديّ أوّليّ». أعطِ مثالًا مضادًّا.", M(r"15=3\times5"))]
    c = r.choice([24, 36, 48, 60])
    rows = [d for d in range(2, c) if c % d == 0]
    problems = [(f"نريد ترتيب {c} كرسيًّا في صفوف متساوية. اكتب كل الترتيبات الممكنة (أكثر من صفّ).", "، ".join(f"{d}×{c // d}" for d in rows)),
                ("علبة فيها بين 30 و40 حبّة، ويمكن توزيعها في أكياس من 4 ومن 6 دون باقٍ. كم حبّة فيها؟", M("36")),
                ("أوجد عددين أوّليّين مجموعهما 24 (كل الحلول).", M("5+19\\ ;\\ 7+17\\ ;\\ 11+13"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_powers(r):
    drill = []
    for _ in range(3):
        a, n = r.randint(2, 9), r.randint(2, 3)
        drill.append((M(f"{a}^{{{n}}}=\\ ?"), M(a ** n)))
    for _ in range(2):
        a, n = r.randint(2, 9), r.randint(3, 5)
        drill.append((f"اكتب على شكل قوّة: {M(TIMES.join([str(a)] * n))}", M(f"{a}^{{{n}}}")))
    for _ in range(3):
        m, k = r.randint(12, 987), r.randint(3, 7)
        drill.append((f"اكتب كعدد مضروب بقوّة للعشرة: {M(g(m * 10 ** k))}", M(rf"{m}\times10^{{{k}}}")))
    x, k = F(r.randint(1001, 9999), 1000), r.randint(1, 3)
    varied = [(f"احسب: {M(dec(x) + TIMES + '10^{' + str(k) + '}')}", M(dec(x * 10 ** k))),
              (f"احسب: {M('2^3' + TIMES + '5^2')} و{M('3^2' + TIMES + '10^2')}", M(r"200\ ;\ 900")),
              ("قارن: " + M("3^4") + " و" + M("4^3"), M("81>64")),
              ("أوجد العدد الذي مربّعه 169 والعدد الذي مكعّبه 64.", M(r"13\ ;\ 4"))]
    problems = [("مكتبة فيها 10 خزائن، في كل خزانة 10 رفوف، على كل رفّ 10 كتب. كم كتابًا؟ اكتب الجواب كقوّة.", M(r"10^3=1000")),
                ("مكعّب كبير ضلعه 5 مكعّبات صغيرة. كم مكعّبًا صغيرًا فيه؟", M(r"5^3=125")),
                ("بلاط غرفة مربّعة: 12 بلاطة في كل صفّ و12 صفًّا. كم بلاطة؟ اكتب الجواب كقوّة.", M(r"12^2=144"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_lcmgcd(r):
    drill = []
    for _ in range(4):
        k = r.randint(2, 9); a, b = k * r.randint(2, 9), k * r.randint(2, 9)
        if a == b:
            b += k
        drill.append((f"أوجد ق.م.أ.ك({a}؛{b})", M(math.gcd(a, b))))
    for _ in range(4):
        a, b = r.randint(3, 15), r.randint(3, 15)
        if a == b:
            b += 2
        drill.append((f"أوجد م.م.أ.ص({a}؛{b})", M(a * b // math.gcd(a, b))))
    a, b = r.randint(8, 30), r.randint(8, 30)
    varied = [(f"أكمل لـ {M(f'a={a}')} و{M(f'b={b}')}: ق.م.أ.ك، م.م.أ.ص، ثم تحقّق أنّ ق.م.أ.ك × م.م.أ.ص = {M('a' + TIMES + ' b')}.",
               M(rf"{math.gcd(a, b)}\ ;\ {a * b // math.gcd(a, b)}\ ;\ {math.gcd(a, b)}\times{a * b // math.gcd(a, b)}={a * b}")),
              ("هل 35 و48 أوّليّان فيما بينهما؟ علّل.", "نعم: ق.م.أ.ك = 1"),
              ("هل 51 و85 أوّليّان فيما بينهما؟ علّل.", "لا: ق.م.أ.ك = 17"),
              ("صحّح: م.م.أ.ص(6؛9) = 54.", M("18"))]
    t1, t2 = r.choice([(8, 12), (10, 15), (12, 20), (6, 16)])
    l1, l2 = r.choice([(84, 126), (60, 90), (72, 120), (45, 75)])
    problems = [(f"حافلتان تنطلقان معًا الساعة 7:00: الأولى كل {t1} دقيقة والثانية كل {t2} دقيقة. متى تنطلقان معًا مجدّدًا؟",
                 f"بعد {t1 * t2 // math.gcd(t1, t2)} دقيقة"),
                (f"شريطان طولهما {l1} cm و{l2} cm نقصّهما إلى قطع متساوية بأكبر طول ممكن دون بقايا. ما طول القطعة؟ وكم قطعة؟",
                 f"{math.gcd(l1, l2)} cm؛ {l1 // math.gcd(l1, l2) + l2 // math.gcd(l1, l2)} قطعة"),
                ("لدينا 36 تفّاحة و48 برتقالة. نريد أكبر عدد من السلال المتماثلة. كم سلّة؟ وماذا في كلٍّ منها؟", "12 سلّة: 3 تفّاحات و4 برتقالات")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_irreducible(r):
    drill = []
    for _ in range(6):
        a, b = r.randint(1, 9), r.randint(2, 12)
        while math.gcd(a, b) != 1 or a >= b:
            a, b = r.randint(1, 9), r.randint(2, 12)
        k = r.randint(2, 12)
        drill.append((f"اختزل: {frc(a * k, b * k)}", M(fr(F(a, b)))))
    for _ in range(2):
        b = r.choice([4, 5, 20, 25, 50]); a = r.randint(1, b - 1)
        drill.append((f"اكتب بمقام 100: {frc(a, b)}", M(rf"\frac{{{a * 100 // b}}}{{100}}")))
    varied = [("ما الكسران الممثَّلان؟ هل هما متكافئان؟ [[fig:fbar|3|2|6|4]]", M(r"\frac23=\frac46")),
              ("أطرد الدخيل: " + M(r"\frac{12}{16}\ ;\ \frac{15}{20}\ ;\ \frac{18}{24}\ ;\ \frac{20}{25}"), M(r"\frac{20}{25}=\frac45")),
              ("أكمل: " + M(r"\frac{5}{7}=\frac{\square}{42}=\frac{45}{\square}"), M(r"30\ ;\ 63")),
              ("قارن بعد الاختزال: " + M(r"\frac{21}{28}") + " و" + M(r"\frac{24}{30}"), M(r"\frac34<\frac45"))]
    problems = [("في مدرسة 480 طالبًا، منهم 180 يأتون بالحافلة. اكتب الكسر مختزلًا.", M(r"\frac{3}{8}")),
                ("قرأ علي 45 صفحة من كتاب فيه 120 صفحة. ما الكسر المقروء؟ (مختزلًا)", M(r"\frac{3}{8}")),
                ("حصلت هند على 27 من 30. اكتب علامتها ككسر مختزل ثم على 100.", M(r"\frac{9}{10}=\frac{90}{100}"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_decfrac(r):
    drill = []
    for _ in range(4):
        k = r.randint(1, 3); n = r.randint(1, 10 ** (k + 1))
        drill.append((f"اكتب عددًا عشريًّا: {frc(n, 10 ** k)}", M(dec(F(n, 10 ** k)))))
    for _ in range(4):
        x = F(r.choice([25, 75, 125, 375, 5, 35, 64, 8, 45]), r.choice([100, 1000]))
        drill.append((f"اكتب كسرًا مختزلًا: {M(dec(x))}", M(fr(x))))
    varied = [("ما الكسر العشريّ والعدد العشريّ الملوّن؟ [[fig:grid|48]]", M(r"\frac{48}{100}=0.48")),
              ("حوّل إلى عدد عشريّ: " + M(r"\frac34\ ;\ \frac25\ ;\ \frac{7}{8}"), M(r"0.75\ ;\ 0.4\ ;\ 0.875")),
              ("رتّب تصاعديًّا: " + M(r"0.6\ ;\ \frac{1}{2}\ ;\ 0.55\ ;\ \frac{3}{5}"), M(r"\frac12<0.55<0.6=\frac35")),
              ("اكتشف الخطأ: " + M(r"\frac{9}{100}=0.9"), M(r"\frac{9}{100}=0.09"))]
    problems = [("في الوصفة " + M(r"1\tfrac14") + " كيلو طحين و" + M(r"\frac34") + " كيلو سكّر. حوّل إلى أعداد عشريّة واجمع.", M(r"1.25+0.75=2")),
                ("ثمن قلم " + M(r"\frac{3}{5}") + " دولار. اكتبه عددًا عشريًّا ثم احسب ثمن 5 أقلام.", M(r"0.6\ ;\ 3")),
                ("مع سامي " + M(r"2\tfrac12") + " دولار ومع أخيه " + M(r"1\tfrac{3}{4}") + " دولار. كم معهما؟ (بالأعداد العشريّة)", M(r"4.25"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_decexp(r):
    drill = []
    for _ in range(4):
        x = F(r.randint(10000, 99999), 1000)
        drill.append((f"دوّر إلى الأعشار ثم اقتطع إلى الأعشار: {M(dec(x))}",
                      M(rf"{dec(F(rnd(x * 10), 10), 1)}\ ;\ {dec(F(math.floor(x * 10), 10), 1)}")))
    for _ in range(4):
        x = F(r.randint(1000, 99999), 100)
        drill.append((f"دوّر إلى أقرب وحدة: {M(dec(x, 2))}", M(rnd(x))))
    varied = [("فصّل وفق قوى 10 و" + M(r"\frac1{10}") + ": " + M("406.25"), M(r"4\times100+6+\frac2{10}+\frac5{100}")),
              ("اكتب العدد: " + M(r"3\times10+7+\frac{4}{100}"), M("37.04")),
              ("رتّب تصاعديًّا: " + M(r"3.5\ ;\ 3.45\ ;\ 3.405\ ;\ 3.54"), M(r"3.405<3.45<3.5<3.54")),
              ("ما رقم الأجزاء من مئة في " + M("12.674") + "؟ وما الجزء الصحيح؟", M(r"7\ ;\ 12"))]
    problems = [("سعر 3 أغراض: " + M(r"5.49\ ;\ 2.75\ ;\ 8.30") + " دولار. قدّر المجموع بتدوير كل سعر إلى أقرب دولار، ثم احسب الدقيق.", M(r"5+3+8=16\ ;\ 16.54")),
                ("وزن حقيبة " + M("7.46") + " كيلو. ماذا يعرض ميزان يدوّر إلى الأعشار؟ وميزان يقتطع إلى الأعشار؟", M(r"7.5\ ;\ 7.4")),
                ("سجّل عدّاء " + M("12.847") + " ثانية. اكتب الوقت مدوّرًا إلى الأجزاء من مئة.", M("12.85"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_fracmul(r):
    drill = []
    for _ in range(4):
        a, b, c, d = r.randint(1, 8), r.randint(2, 9), r.randint(1, 8), r.randint(2, 9)
        drill.append((M(rf"\frac{{{a}}}{{{b}}}\times\frac{{{c}}}{{{d}}}"), M(fr(F(a, b) * F(c, d)))))
    for _ in range(4):
        a, b, c, d = r.randint(1, 8), r.randint(2, 9), r.randint(1, 8), r.randint(2, 9)
        drill.append((M(rf"\frac{{{a}}}{{{b}}}\div\frac{{{c}}}{{{d}}}"), M(fr(F(a, b) / F(c, d)))))
    n, dd = r.choice([(3, 4), (2, 5), (5, 6), (3, 8)]); q = dd * r.randint(4, 12)
    varied = [(f"احسب {frc(n, dd)} من {q}.", M(n * q // dd)),
              ("اكتب مقلوب: " + M(r"\frac{4}{7}\ ;\ 9\ ;\ \frac{1}{6}"), M(r"\frac74\ ;\ \frac19\ ;\ 6")),
              ("ماذا يمثّل الجزء المشترك؟ [[fig:fbar|4|3|2|1]]", M(r"\frac34\times\frac12=\frac38")),
              ("اكتشف الخطأ: " + M(r"\frac23\times\frac34=\frac{5}{7}"), M(r"\frac{6}{12}=\frac12"))]
    problems = [("لدينا 12 لترًا من العصير نصبّها في قوارير سعة كلّ منها " + M(r"\frac34") + " لتر. كم قارورة؟", M("16")),
                ("مع هادي 150 دولارًا. صرف " + M(r"\frac25") + " منها على الكتب. كم صرف؟ وكم بقي؟", M(r"60\ ;\ 90")),
                ("بقي " + M(r"\frac23") + " قالب الكعك، وأكلنا " + M(r"\frac14") + " الباقي. ما الجزء المأكول من القالب كلّه؟", M(r"\frac16"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_rationals(r):
    xs = r.sample([x for x in range(-9, 10) if x], 6)
    drill = [(f"اكتب نظير {M(sg(x))}", M(sg(-x))) for x in xs]
    drill += [(f"عبّر بعدد نسبيّ: {t}", M(v)) for t, v in r.sample([("ربح 50 دولارًا", "+50"), ("خسارة 15 دولارًا", "-15"), ("الطابق الثالث تحت الأرض", "-3"),
                                                                     ("12 درجة فوق الصفر", "+12"), ("عمق 40 m تحت سطح البحر", "-40")], 2)]
    a, b, c = sorted(r.sample(range(-5, 6), 3))
    t0, u1, d1, u2 = 0, r.randint(2, 8), r.randint(5, 15), r.randint(1, 9)
    varied = [(f"ما فواصل النقاط؟ [[fig:nl|-5|5|1|A@{a}|B@{b}|C@{c}]]", M(rf"A({a})\ ;\ B({b})\ ;\ C({c})")),
              (f"ابدأ من {deg(0)}: ارتفاع {u1}، ثم انخفاض {d1}، ثم ارتفاع {u2}. ما الحرارة النهائيّة؟", M(sg(u1 - d1 + u2) + r"^\circ")),
              ("عددان متناظران البعد بينهما على المحور 18 وحدة. ما هما؟", M(r"-9\ ;\ +9")),
              ("ضع على محور: " + M(r"-3.5\ ;\ +2\ ;\ -1\ ;\ +4.5"), "رسم")]
    problems = [("غوّاص على عمق 14 m، صعد 6 m ثم نزل 9 m. أين أصبح؟", M("-17") + " m"),
                ("ركب رامي المصعد من الطابق " + M("-3") + " إلى الطابق " + M("+4") + ". كم طابقًا صعد؟", M("7")),
                ("حصلت فرق على نقاط: 14، 7، 10، 3 من 20. عبّر عن بعد كل نتيجة عن 10 بعدد نسبيّ.", M(r"+4\ ;\ -3\ ;\ 0\ ;\ -7"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_compare(r):
    drill = []
    for _ in range(6):
        a, b = r.sample(range(-20, 21), 2)
        drill.append((M(rf"{a}\ \square\ {b}"), M(f"{a}{'<' if a < b else '>'}{b}")))
    for _ in range(2):
        xs = r.sample(range(-15, 16), 5)
        drill.append((f"رتّب تصاعديًّا: {'؛ '.join(M(x) for x in xs)}", M("<".join(map(str, sorted(xs))))))
    varied = [("أيّ النقطتين فاصلتها أكبر؟ [[fig:nl|-8|2|1|A@-7|B@-3]]", M(r"B:\ -3>-7")),
              ("رتّب تنازليًّا: " + M(r"-2.5\ ;\ 1.4\ ;\ -2.05\ ;\ 0\ ;\ -3"), M(r"1.4>0>-2.05>-2.5>-3")),
              ("اكتب كل الأعداد الصحيحة بين " + M("-4") + " و" + M("+3") + ".", M(r"-3,-2,-1,0,1,2")),
              ("قارن: " + M(r"-\frac34") + " و" + M(r"-\frac23"), M(r"-\frac34<-\frac23"))]
    problems = [("حرارة 5 مدن: " + M(r"-7^\circ\ ;\ 3^\circ\ ;\ -12^\circ\ ;\ 0^\circ\ ;\ -1^\circ") + ". رتّبها من الأبرد إلى الأدفأ.", M(r"-12<-7<-1<0<3")),
                ("أرباح شركة (آلاف الدولارات): " + M(r"+8\ ;\ -3\ ;\ +5\ ;\ -9") + ". ما الشهر الأسوأ؟", M("-9")),
                ("غوّاصتان على عمق " + M("-120") + " m و" + M("-85") + " m. أيّهما أعمق؟", M(r"-120<-85"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_addsub(r):
    drill = []
    for i in range(8):
        a, b = r.randint(-15, 15), r.randint(-15, 15)
        if i < 4:
            drill.append((M(f"({sg(a)})+({sg(b)})"), M(a + b)))
        else:
            drill.append((M(f"({sg(a)})-({sg(b)})"), M(a - b)))
    a, b, c, d = (r.randint(-12, 12) for _ in range(4))
    varied = [(M(f"({sg(a)})+({sg(b)})-({sg(c)})+({sg(d)})"), M(a + b - c + d)),
              ("أكمل: " + M(rf"({sg(a)})+\square={b}"), M(b - a)),
              ("استعمل المحور: " + M("(-4)+(+7)") + " [[fig:nl|-5|5|1|-4|3]]", M("+3")),
              ("اكتشف الخطأ: " + M(r"(-6)-(-2)=-8"), M(r"(-6)+(+2)=-4"))]
    problems = [("في الحافلة 27 راكبًا: نزل 8، صعد 5، نزل 11، صعد 3. كم راكبًا الآن؟", M("16")),
                ("كانت الحرارة " + M(r"-6^\circ") + " صباحًا و" + M(r"+9^\circ") + " ظهرًا. كم ارتفعت؟", M(r"15^\circ")),
                ("رصيد حساب " + M("-25") + " دولارًا. أُودِع 60 ثم سُحب 18. ما الرصيد؟", M("+17"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_lines(r):
    drill = []
    for _ in range(4):
        rr = r.randint(2, 9)
        if r.random() < .5:
            drill.append((f"دائرة شعاعها {rr} cm. ما قطرها؟", f"{2 * rr} cm"))
        else:
            drill.append((f"دائرة قطرها {2 * rr} cm. ما شعاعها؟", f"{rr} cm"))
    for _ in range(4):
        rr, d = r.randint(3, 6), r.randint(1, 8)
        pos = "داخل الدائرة" if d < rr else ("على الدائرة" if d == rr else "خارج الدائرة")
        drill.append((f"دائرة شعاعها {rr} cm ونقطة M حيث OM = {d} cm. أين تقع M؟", pos))
    varied = [("ما وضعيّة المستقيم (d) بالنسبة إلى الدائرة؟ [[fig:circ|4|2]]", "قاطع: 2 &lt; 4"),
              ("ما وضعيّة المستقيم (d)؟ [[fig:circ|3|3]]", "مماسّ: d = r"),
              ("سمِّ العناصر [OA]، [BC]، [DE]. [[fig:circparts]]", "شعاع؛ قطر؛ وتر"),
              ("ما العلاقة بين المستقيمين؟ وكيف نقيس المسافة بينهما؟ [[fig:lines|par]]", "متوازيان؛ بقطعة عموديّة عليهما")]
    problems = [("عنزة مربوطة بحبل 5 m. شجرة على بعد 4 m، وبئر على بعد 7 m. ماذا تصل؟", "الشجرة فقط"),
                ("بين عمودين 30 m. نضع 5 أعمدة بينهما على مسافات متساوية. ما المسافة بين كل عمودين متتاليين؟", "5 m"),
                ("ما أطول وتر في دائرة شعاعها 7 cm؟", "القطر: 14 cm")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_angles(r):
    drill = []
    for _ in range(3):
        a = r.randint(10, 80)
        drill.append((f"متمّمة الزاوية {deg(a)}", M(rf"{90 - a}^\circ")))
    for _ in range(3):
        a = r.randint(15, 165)
        drill.append((f"مكمّلة الزاوية {deg(a)}", M(rf"{180 - a}^\circ")))
    for _ in range(2):
        a = r.choice([35, 50, 65, 80, 110, 125, 140])
        kind = "حادّة" if a < 90 else "منفرجة"
        drill.append((f"صنّف الزاوية {deg(a)}", kind))
    a, b = r.randint(25, 70), r.randint(30, 80)
    v = r.randint(25, 75)
    varied = [(f"احسب الزاوية x. [[fig:lin|{180 - v}]]", M(rf"x={v}^\circ")),
              (f"مستقيمان متقاطعان. ما قياس الزاوية المشار إليها بـ «؟»؟ [[fig:vert|{v}]]", M(rf"{v}^\circ")),
              (f"{M(hat('xOz') + f'={a}' + DEG)} و{M(hat('zOy') + f'={b}' + DEG)} متجاورتان. احسب {M(hat('xOy'))}. [[fig:adj|{a}|{b}]]", M(rf"{a + b}^\circ")),
              (f"[Oz) منصّف {M(hat('xOy') + f'={2 * a}' + DEG)}. احسب {M(hat('xOz'))}.", M(rf"{a}^\circ"))]
    problems = [("زاويتان متقابلتان بالرأس: " + M(r"(2x+20)^\circ") + " و" + M(r"(4x-10)^\circ") + ". أوجد x وقياس كلّ منهما.", M(r"x=15\ ;\ 50^\circ")),
                ("زاويتان متكاملتان، إحداهما أربعة أضعاف الأخرى. احسبهما.", M(r"36^\circ\ ;\ 144^\circ")),
                ("ما الزاوية بين عقربَي الساعة عند الثانية؟ وعند السادسة؟", M(r"60^\circ\ ;\ 180^\circ"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_triangles(r):
    drill = []
    for _ in range(4):
        a, b = r.randint(25, 80), r.randint(25, 80)
        drill.append((f"زاويتان في مثلّث: {deg(a)} و{deg(b)}. احسب الثالثة.", M(rf"{180 - a - b}^\circ")))
    for _ in range(2):
        apex = r.choice([20, 40, 50, 70, 80, 100, 120])
        drill.append((f"مثلّث متساوي الساقين زاوية رأسه {deg(apex)}. احسب زاويتي القاعدة.", M(rf"{(180 - apex) // 2}^\circ")))
    for _ in range(2):
        b = r.randint(20, 70)
        drill.append((f"مثلّث قائم إحدى زاويتيه الحادّتين {deg(b)}. احسب الأخرى.", M(rf"{90 - b}^\circ")))
    a, b = r.randint(35, 75), r.randint(35, 75)
    varied = [(f"احسب الزاوية الناقصة وصنّف المثلّث. [[fig:tri|{a}|{b}]]", M(rf"{180 - a - b}^\circ") + (" حادّ الزوايا" if max(a, b, 180 - a - b) < 90 else (" قائم" if max(a, b, 180 - a - b) == 90 else " منفرج"))),
              ("احسب زاويتي القاعدة. [[fig:iso|50]]", M(r"65^\circ")),
              ("هل يمكن رسم مثلّث زواياه " + M(r"95^\circ\ ;\ 60^\circ\ ;\ 35^\circ") + "؟", "لا: المجموع " + M(r"190^\circ")),
              ("ما اسم المستقيم الذي يصل رأسًا بمنتصف الضلع المقابل؟", "المتوسّط")]
    problems = [("زوايا مثلّث: " + M(r"x\ ;\ 2x\ ;\ 3x") + ". احسبها وصنّف المثلّث.", M(r"30^\circ,60^\circ,90^\circ") + " قائم"),
                ("سقف متساوي الساقين زاوية رأسه " + M(r"130^\circ") + ". احسب زاويتي القاعدة.", M(r"25^\circ")),
                ("كيف نجد مكانًا على البعد نفسه من ثلاث قرى؟", "تقاطع المنصّفات العموديّة لأضلاع المثلّث")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_areas(r):
    drill = []
    for _ in range(2):
        L, l = r.randint(4, 15), r.randint(2, 10)
        drill.append((f"مساحة مستطيل {L} cm × {l} cm ومحيطه", f"{L * l} cm²؛ {2 * (L + l)} cm"))
    for _ in range(2):
        a = r.randint(3, 12)
        drill.append((f"مساحة مربّع ضلعه {a} cm ومحيطه", f"{a * a} cm²؛ {4 * a} cm"))
    for _ in range(2):
        b, h = r.randint(4, 16), r.randint(2, 12)
        drill.append((f"مساحة مثلّث قاعدته {b} cm وارتفاعه {h} cm", f"{b * h / 2:g} cm²"))
    for _ in range(2):
        b, h = r.randint(4, 14), r.randint(2, 9)
        drill.append((f"مساحة متوازي أضلاع قاعدته {b} cm وارتفاعه {h} cm", f"{b * h} cm²"))
    B, bb, h = r.choice([(12, 8, 5), (10, 6, 4), (14, 6, 3), (9, 5, 6)])
    W, H, w, hh = r.choice([(10, 7, 4, 3), (9, 6, 3, 2), (12, 8, 5, 4)])
    varied = [(f"احسب المساحة. [[fig:shape|trap|{B}|{bb}|{h}]]", f"{(B + bb) * h // 2} cm²"),
              (f"احسب مساحة الشكل. [[fig:shape|L|{W}|{H}|{w}|{hh}]]", f"{W * H - w * hh} cm²"),
              ("احسب المساحة. [[fig:shape|rtri|10|6]]", "30 cm²"),
              ("مستطيل مساحته 54 cm² وطوله 9 cm. احسب عرضه ومحيطه.", "6 cm؛ 30 cm")]
    problems = [("غرفة " + M(r"5\times4") + " m، ثمن المتر المربّع من البلاط 15 دولارًا. ما الكلفة؟", "300 دولار"),
                ("حديقة مربّعة مساحتها 49 m². ما محيطها؟", "28 m"),
                ("بـ 20 m سياج: ما أبعاد المستطيل الذي يعطي أكبر مساحة؟", M(r"5\times5=25") + " m²")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_ratio(r):
    drill = []
    for _ in range(4):
        k = r.randint(2, 9); a, b = r.randint(1, 9), r.randint(1, 9)
        while math.gcd(a, b) != 1 or a == b:
            a, b = r.randint(1, 9), r.randint(1, 9)
        drill.append((f"اكتب في أبسط صورة: {M(f'{a * k}:{b * k}')}", M(f"{a}:{b}")))
    for _ in range(2):
        v, t = r.randint(4, 12) * 10, r.randint(2, 5)
        drill.append((f"قطعت سيّارة {v * t} km في {t} ساعات. ما سرعتها؟", f"{v} km/h"))
    for _ in range(2):
        p, n = r.randint(2, 9) * 500, r.randint(3, 8)
        drill.append((f"{n} أقلام بـ {M(g(p * n))} ليرة. ما سعر القلم؟", M(g(p)) + " ليرة"))
    varied = [("احسب نسبة 25 cm إلى 1 m.", M(r"\frac14")),
              ("ما نسبة الجزء الملوّن إلى غير الملوّن؟ [[fig:fbar|7|4]]", M("4:3")),
              ("اكتشف الخطأ: نسبة 300 g إلى 2 kg هي 150.", M(r"\frac{300}{2000}=\frac{3}{20}")),
              ("اكتب كسرًا ثم عددًا عشريًّا: حاصل قسمة 7 على 8.", M(r"\frac78=0.875"))]
    problems = [("نوزّع 72 كرة بين فريقين بنسبة " + M("4:5") + ". كم لكلّ فريق؟", M(r"32\ ;\ 40")),
                ("وصفة: 2 كوب أرزّ لكل 3 أكواب ماء. كم كوب ماء لـ 8 أكواب أرزّ؟", M("12")),
                ("على خريطة مقياسها " + M(r"1:50\,000") + "، المسافة 6 cm. ما المسافة الحقيقيّة بالكيلومتر؟", "3 km")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_literal(r):
    drill = []
    for _ in range(4):
        a, b, x = r.randint(2, 9), r.randint(1, 15), r.randint(1, 9)
        drill.append((f"احسب {M(f'{a}x+{b}')} عندما {M(f'x={x}')}", M(a * x + b)))
    for _ in range(2):
        k, a = r.randint(2, 9), r.randint(1, 9)
        drill.append((f"وسّع: {M(f'{k}(x+{a})')}", M(f"{k}x+{k * a}")))
    for _ in range(2):
        a, b, c, d = r.randint(2, 9), r.randint(1, 9), r.randint(1, 5), r.randint(1, 9)
        drill.append((f"اختزل: {M(f'{a}x+{b}+{c}x+{d}')}", M(f"{a + c}x+{b + d}")))
    varied = [("اكتب عبارة: «7 أكثر من ثلاثة أضعاف x»؛ «نصف y»؛ «الفرق بين a و9».", M(r"3x+7\ ;\ \frac{y}{2}\ ;\ a-9")),
              ("صح أم خطأ: " + M("5x-2=13") + " عندما " + M("x=3") + "؟", "صحيح"),
              ("اكتشف الخطأ: " + M("4x+3=7x"), "حدّان غير متشابهين، لا تُجمع"),
              ("وسّع واختزل: " + M("3(x+4)-x"), M("2x+12"))]
    problems = [("عمر الأب ضعف عمر ابنه x زائد 6. اكتب عبارة لعمر الأب واحسبها عندما " + M("x=14") + ".", M(r"2x+6\ ;\ 34")),
                ("ثمن التذكرة x دولار للكبير و4 دولارات للصغير. ذهب كبيران و3 صغار. اكتب عبارة واحسبها عندما " + M("x=9") + ".", M(r"2x+12\ ;\ 30")),
                ("مستطيل طوله " + M("x+5") + " وعرضه x. اكتب عبارة لمحيطه واحسبه عندما " + M("x=4") + ".", M(r"4x+10\ ;\ 26"))]
    return dict(drill=drill, varied=varied, problems=problems)


def w_percent(r):
    drill = []
    for _ in range(4):
        p, a = r.choice([10, 20, 25, 50, 5, 15, 30, 75]), r.randint(2, 30) * 20
        drill.append((f"احسب {p}% من {a}", M(f"{p * a / 100:g}")))
    for _ in range(4):
        tot = r.choice([20, 25, 40, 50, 80]); part = r.randint(1, tot - 1)
        while (part * 100) % tot:
            part = r.randint(1, tot - 1)
        drill.append((f"ما النسبة المئويّة لـ {part} من {tot}؟", f"{part * 100 // tot}%"))
    varied = [("ما النسبة المئويّة الملوّنة؟ [[fig:grid|62]]", "62%"),
              ("ما النسبة المئويّة للجزء الملوّن؟ [[fig:pie|3|4]]", "75%"),
              ("اكتب كسرًا مختزلًا: 40%؛ 5%؛ 12%", M(r"\frac25\ ;\ \frac1{20}\ ;\ \frac{3}{25}")),
              ("اكتشف الخطأ: 20% من 60 هي 40.", "هي 12")]
    problems = [("قميص بـ 80 دولارًا عليه حسم 15%. كم ندفع؟", "68 دولارًا"),
                ("راتب 250 دولارًا زاد 12%. كم أصبح؟", "280 دولارًا"),
                ("في صفّ 30 طالبًا: 12 يحبّون الرسم والباقي الرياضة. ما النسبة المئويّة لكلّ فئة؟", "40%؛ 60%")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_proportional(r):
    drill = []
    for _ in range(4):
        k = r.randint(2, 9); xs = r.sample(range(1, 10), 3)
        drill.append((f"جدول تناسب معامله {k}: أكمل {xs[0]} ← ؟، {xs[1]} ← ؟، {xs[2]} ← ؟", "، ".join(str(k * x) for x in xs)))
    for _ in range(4):
        a, b = r.randint(2, 9), r.randint(2, 9); c = a * r.randint(2, 5)
        drill.append((f"أوجد x: {M(frc(a, b)[2:-2] + '=' + frc(c, 'x')[2:-2])}", M(f"x={b * c // a}")))
    varied = [("أكمل جدول التناسب: <table class='mini'><tr><th>الكيلو</th><td>2</td><td>5</td><td>?</td></tr><tr><th>الثمن</th><td>6</td><td>?</td><td>24</td></tr></table>", "15؛ 8"),
              ("هل 2، 5، 8 ← 7، 17.5، 28 جدول تناسب؟", "نعم: المعامل 3.5"),
              ("هل 1، 2، 3 ← 4، 6، 8 جدول تناسب؟ علّل.", "لا: " + M(r"\frac41\neq\frac62")),
              ("هل محيط المربّع متناسب مع ضلعه؟", "نعم: المعامل 4")]
    problems = [("4 كيلو تفّاح بـ 120 000 ليرة. كم ثمن 7 كيلو؟", M(r"210\,000") + " ليرة"),
                ("سيّارة تستهلك 8 لترات لكل 100 km. كم لترًا لـ 250 km؟", "20 لترًا"),
                ("وصفة لـ 6 أشخاص تحتاج 450 g طحين. كم نحتاج لـ 10 أشخاص؟", "750 g")]
    return dict(drill=drill, varied=varied, problems=problems)


def w_stats(r):
    drill = []
    for _ in range(4):
        xs = r.sample(range(5, 21), r.choice([5, 6]))
        xs.append(r.choice(xs))                     # exactly one repeated value: a single mode
        r.shuffle(xs)
        s = sorted(xs)
        med = F(s[len(s) // 2 - 1] + s[len(s) // 2], 2) if len(s) % 2 == 0 else s[len(s) // 2]
        mode = max(set(xs), key=xs.count)
        drill.append((f"البيانات: {'، '.join(map(str, xs))}. أوجد المدى والمنوال والوسيط.",
                      f"المدى {max(xs) - min(xs)}؛ المنوال {mode}؛ الوسيط {M(fr(med) if isinstance(med, F) else med)}"))
    vals = [r.randint(2, 12) for _ in range(5)]
    days = "إث,ثل,أر,خم,جم"
    varied = [(f"في أيّ يوم أكبر قيمة؟ وما مجموع القيم؟ [[fig:bars|{days}|{','.join(map(str, vals))}]]",
               f"{['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'][vals.index(max(vals))]}؛ {sum(vals)}"),
              ("أوجد المدى والمنوال. [[fig:dots|2,3,3,4,4,4,5,6]]", "المدى 4؛ المنوال 4"),
              ("ما أكبر ارتفاع بين يومين متتاليين؟ [[fig:line|1,2,3,4,5|14,18,15,22,20]]", "بين 3 و4: 7"),
              ("لمتابعة طول نبتة خلال شهر، أيّ تمثيل تختار؟", "تمثيل بالخطوط")]
    problems = [("علامات 6 طلّاب: 14، 17، 11، 17، 19، 12. أوجد الوسيط.", M(r"\frac{14+17}{2}=15.5")),
                ("اكتب 5 أعداد مداها 8 ومنوالها 10 ووسيطها 10.", "مثال: 6، 9، 10، 10، 14"),
                ("سألنا 20 شخصًا عن ساعات الرياضة: 0 (2)، 1 (6)، 2 (7)، 3 (5). ما المنوال؟", "2 ساعة")]
    return dict(drill=drill, varied=varied, problems=problems)


GEN = {"naturals": w_naturals, "order": w_order, "primes": w_primes, "powers": w_powers, "lcm-gcd": w_lcmgcd, "irreducible": w_irreducible,
       "dec-fractions": w_decfrac, "dec-expand": w_decexp, "frac-mul": w_fracmul, "rationals": w_rationals, "compare": w_compare, "add-sub": w_addsub,
       "lines-circles": w_lines, "angles": w_angles, "triangles": w_triangles, "areas": w_areas, "ratio": w_ratio, "literal": w_literal,
       "percent": w_percent, "proportional": w_proportional, "stats": w_stats}


# ---------------------------------------------------------------- page assembly
SECTIONS = [("drill", "أ", "تمارين سريعة", "أجب في الفراغ."), ("varied", "ب", "تمارين متنوّعة", "اقرأ السؤال والرسم جيّدًا، ثم أجب."),
            ("problems", "ج", "مسائل من الحياة", "اكتب خطوات الحلّ.")]


def sheet(L, data, first):
    secs = []
    k = 0
    for key, letter, name, instr in SECTIONS:
        lis = []
        for q, _ in data[key]:
            k += 1
            wide = key == "problems" or "[[fig:" in q or "<table" in q or len(re.sub(r"\\\(.*?\\\)", "xx", q)) > 70
            lines = '<i class="wb-ans"></i>' * (5 if key == "problems" else 1)
            lis.append(f'<li class="{"wide" if wide else ""}"><span class="q-n">{k}</span><div class="wb-q"><p>{q}</p>{lines}</div></li>')
        secs.append(f'<div class="wb-sec wb-{key}"><h3><span>{letter}</span>{name}<small>{instr}</small></h3><ol class="wb-list">{"".join(lis)}</ol></div>')
    return f'''
<section class="sheet wb c-{L["color"]}" id="{L["id"]}">
  <header class="wb-h">{build.mk(L["id"])}<div class="wb-num">{L["num"]}</div>
    <div><p class="eyebrow">ورقة عمل {L["num"]} · المحور {L["unit"]}</p><h2>{L["title"]}</h2></div>
    <div class="wb-meta"><span>الاسم: ....................</span><span>التاريخ: ......./......./.......</span><span class="wb-score">العلامة: ...... / {k}</span></div>
  </header>
  {"".join(secs)}
  <p class="wb-self">كيف كان أدائي؟ <span>☆</span><span>☆</span><span>☆</span> · أحتاج إلى مراجعة: .......................................</p>
</section>'''


def key_page(L, data):
    rows, k = [], 0
    for key, letter, name, _ in SECTIONS:
        for _, a in data[key]:
            k += 1
            rows.append(f'<li><span class="a-n">{k}</span><div>{a}</div></li>')
    return f'<div class="wbk c-{L["color"]}"><h3><span>{L["num"]}</span>{L["title"]}</h3><ol>{"".join(rows)}</ol></div>'


def cover():
    c = build.cover()
    c = c.replace('<h1>رياضيات<br><span>الصفّ السادس</span></h1>', '<h1>كتاب التمارين<br><span>رياضيات الصفّ السادس</span></h1>')
    return c


def intro_page():
    units = "".join(f'<li class="c-{U["color"]}"><b>المحور {U["num"]}</b> {U["title"]}: أوراق العمل '
                    f'{", ".join(str(L["num"]) for L in LESSONS if L["id"] in U["lessons"])}</li>' for U in UNITS)
    return f'''
<section class="sheet wb-intro" id="wb-intro">
  <p class="eyebrow">{build.mk("wb-intro")}كتاب التمارين المرافق</p>
  <h2 class="h-big">تدرّب… ثم تدرّب!</h2>
  <p class="prose-p">في هذا الكتاب <b>21 ورقة عمل</b>، واحدة لكل درس من دروس كتاب «رياضيات الصفّ السادس». كل التمارين جديدة ولا تتكرّر في الكتاب الأساسيّ.
  في كل ورقة ثلاثة أقسام: <b>(أ) تمارين سريعة</b> لتثبيت المهارة، <b>(ب) تمارين متنوّعة</b> برسوم وجداول، و<b>(ج) مسائل من الحياة</b>.
  الحلول في كتيّب منفصل مع المعلّم.</p>
  <ul class="wb-units">{units}</ul>
  <div class="ht-hello">{__import__("extras").owl(90)}<p>نصيحة من <b>نَبيه</b>: حلّ الورقة وحدك أوّلًا، ثم صحّح مع معلّمك، ولوّن نجوم أدائك في أسفل كل ورقة.</p></div>
</section>'''


CSS_EXTRA = r'''
.wb-h { display: grid; grid-template-columns: auto 1fr; gap: 4px 14px; align-items: center; padding-bottom: 8px; border-bottom: 3px solid var(--c); margin-bottom: 10px; }
.wb-num { grid-row: span 2; width: 58px; height: 58px; border-radius: 16px; background: var(--c); color: #fff; display: grid; place-items: center; font-family: var(--f-display); font-size: 1.8rem; font-weight: 800; }
.wb-h h2 { margin: 0; font-family: var(--f-display); font-size: 1.45rem; color: var(--c); }
.wb-h .eyebrow { margin: 0; }
.wb-meta { grid-column: 2; display: flex; flex-wrap: wrap; gap: 4px 18px; font-size: .8rem; color: var(--ink-2); }
.wb-score { margin-inline-start: auto; font-weight: 700; color: var(--c); }
.wb-sec { margin: 10px 0 6px; }
.wb-sec h3 { display: flex; align-items: center; gap: 8px; font-family: var(--f-display); font-size: 1.02rem; margin: 0 0 6px; color: var(--ink); }
.wb-sec h3 span { width: 26px; height: 26px; border-radius: 8px; background: color-mix(in srgb, var(--c) 18%, var(--paper)); color: var(--c); display: grid; place-items: center; }
.wb-sec h3 small { font-weight: 500; font-size: .76rem; color: var(--ink-3); }
.wb-list { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 10px; }
.wb-list li { display: flex; gap: 8px; align-items: flex-start; border: 1px solid var(--line); border-radius: 10px; padding: 6px 10px; break-inside: avoid; }
.wb-list li.wide { grid-column: 1 / -1; }
.wb-q { flex: 1; min-width: 0; }
.wb-q p { margin: 0 0 2px; font-size: .9rem; line-height: 1.7; }
.wb-ans { display: block; height: 22px; border-bottom: 1.5px dotted color-mix(in srgb, var(--ink-3) 60%, var(--paper)); }
.wb-self { margin-top: 10px; padding: 6px 12px; border-radius: 10px; background: color-mix(in srgb, var(--gold) 14%, var(--paper)); font-size: .82rem; }
.wb-self span { color: #E9B44C; font-size: 1.2rem; margin-inline-start: 4px; }
.wb-units { display: grid; gap: 6px; margin: 12px 0; }
.wb-units li { padding: 8px 14px; border-radius: 10px; background: color-mix(in srgb, var(--c) 9%, var(--paper)); border-inline-start: 5px solid var(--c); font-size: .9rem; }
.wb-units b { color: var(--c); font-family: var(--f-display); }
.wbk { break-inside: avoid; border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; margin-bottom: 8px; }
.wbk h3 { display: flex; gap: 8px; align-items: center; margin: 0 0 4px; font-family: var(--f-display); font-size: .92rem; color: var(--c); }
.wbk h3 span { width: 22px; height: 22px; border-radius: 6px; background: var(--c); color: #fff; display: grid; place-items: center; font-size: .72rem; }
.wbk ol { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px 12px; }
.wbk li { display: flex; gap: 6px; font-size: .74rem; line-height: 1.6; }
.wbk .a-n { color: var(--ink-3); min-width: 14px; }
.wb-keygrid { columns: 1; }
@media print { .wb { padding-top: 8mm !important; } .wb-problems { break-before: page; } }
.cover h1 { font-size: 3.1rem; } .cover h1 span { font-size: .72em; }
.wb-problems .wb-list li { padding-bottom: 10px; }
'''


def main():
    datas = {L["id"]: GEN[L["id"]](random.Random(1000 + L["num"])) for L in LESSONS}
    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read() + CSS_EXTRA
    body = cover() + intro_page() + "".join(sheet(L, datas[L["id"]], True) for L in LESSONS)
    build.page(css, "كتاب التمارين · رياضيات الصف السادس", body, "workbook.html")
    keys = "".join(key_page(L, datas[L["id"]]) for L in LESSONS)
    kbody = f'''<section class="sheet ans" id="wb-key"><p class="eyebrow">للمعلّم فقط</p><h2 class="h-big">حلول كتاب التمارين</h2>
  <p class="prose-p">الإجابات النهائيّة لأوراق العمل الـ 21 في «كتاب التمارين – رياضيات الصفّ السادس». الأرقام تتبع ترقيم التمارين في كل ورقة.</p>{keys}</section>'''
    build.page(css, "حلول كتاب التمارين", kbody, "workbook-key.html")
    P = make_pdf.P
    make_pdf.run("node", "pdf.js", "workbook.html", "_wb.pdf", "body")
    found = make_pdf.markers(P("_wb.pdf"))
    make_pdf.run("node", "pdf.js", "workbook.html", "_wbc.pdf", "cover")
    titles = [(1, "مقدّمة", "wb-intro")] + [(1, f'ورقة عمل {L["num"]}: {L["title"]}', L["id"]) for L in LESSONS]
    n = make_pdf.decorate(P("_wb.pdf"), 2, found, BOOK, cover=P("_wbc.pdf"), toc_titles=titles)
    print(f"{BOOK}: {n} pages")
    make_pdf.run("node", "pdf.js", "workbook-key.html", "_wbk.pdf", "body")
    n = make_pdf.decorate(P("_wbk.pdf"), 1, {}, KEY)
    print(f"{KEY}: {n} pages")
    for f in ("_wb.pdf", "_wbc.pdf", "_wbk.pdf"):
        os.remove(P(f))


if __name__ == "__main__":
    main()
