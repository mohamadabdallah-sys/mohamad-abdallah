# -*- coding: utf-8 -*-
"""The book's finishing touches: mascot, «هل تعلم؟» facts, title page, how-to page, journey map, badges, certificate, back cover."""

MASCOT_NAME = "نَبيه"

# ---- the mascot: a friendly owl (colours follow the lesson colour) -----------------
def owl(size=86, cls=""):
    return f'''<svg class="owl {cls}" viewBox="0 0 120 130" width="{size}" height="{size * 130 // 120}" aria-hidden="true">
  <path class="owl-ear" d="M24 34 L30 8 L46 26 Z M96 34 L90 8 L74 26 Z"/>
  <ellipse class="owl-body" cx="60" cy="72" rx="44" ry="50"/>
  <ellipse class="owl-belly" cx="60" cy="88" rx="28" ry="30"/>
  <path class="owl-feather" d="M48 80 q6 6 12 0 q6 6 12 0 M44 94 q8 6 16 0 q8 6 16 0 M48 108 q6 5 12 0 q6 5 12 0"/>
  <circle class="owl-eye" cx="42" cy="50" r="17"/><circle class="owl-eye" cx="78" cy="50" r="17"/>
  <circle class="owl-pupil" cx="45" cy="52" r="7"/><circle class="owl-pupil" cx="75" cy="52" r="7"/>
  <circle class="owl-glint" cx="47" cy="49" r="2.4"/><circle class="owl-glint" cx="77" cy="49" r="2.4"/>
  <path class="owl-beak" d="M54 64 L66 64 L60 74 Z"/>
  <path class="owl-cap" d="M22 30 L60 12 L98 30 L60 44 Z"/><path class="owl-tassel" d="M92 32 V52"/><circle class="owl-tassel-b" cx="92" cy="54" r="4"/>
  <path class="owl-foot" d="M44 120 l-6 6 M48 121 v7 M52 120 l6 6 M68 120 l-6 6 M72 121 v7 M76 120 l6 6"/>
</svg>'''


# ---- one «هل تعلم؟» fact per lesson ------------------------------------------------
FACTS = {
    "naturals": r"الرقم «صفر» وصل إلى العالم عن طريق العلماء العرب، ولولاه لما استطعنا كتابة مليار بعشرة أرقام فقط: \(1\,000\,000\,000\).",
    "order": r"الآلة الحاسبة العلميّة «تعرف» أولويّة العمليّات، أمّا بعض الآلات البسيطة فتحسب بالترتيب، فتعطي \(2+3\times4=20\) بدل 14!",
    "primes": r"أكبر عدد أوّليّ معروف فيه أكثر من 41 مليون رقم! والأعداد الأوّليّة تحمي كلمات السرّ في هاتفك.",
    "powers": r"لو طويت ورقة على نفسها 42 مرّة (\(2^{42}\) طبقة) لوصل سمكها تقريبًا إلى القمر!",
    "lcm-gcd": r"حشرات «الزيز» تخرج من الأرض كل 13 أو 17 سنة، وهما عددان أوّليّان، فنادرًا ما تلتقي بأعدائها!",
    "irreducible": r"في الموسيقى، النوتة «الرابعة» تدوم \(\frac14\) النوتة الكاملة، والموسيقيّون يجمعون الكسور وهم يعزفون.",
    "dec-fractions": r"العالم المسلم غياث الدين الكاشي من أوائل من استعملوا الكسور العشريّة بطريقة منظّمة في القرن الخامس عشر.",
    "dec-expand": r"في سباقات الجري تُقاس الأوقات إلى الأجزاء من مئة من الثانية، وقد يفوز العدّاء بفارق \(0.01\) ثانية فقط!",
    "frac-mul": r"الطبّاخون يضربون الكسور كل يوم: إذا طبخوا نصف وصفة فيها \(\frac34\) كوب سكّر، يحتاجون \(\frac38\) كوب.",
    "rationals": r"أدنى نقطة على اليابسة هي شاطئ البحر الميت، على نحو \(-430\) مترًا تحت سطح البحر.",
    "compare": r"أبرد حرارة سُجّلت على الأرض كانت نحو \(-89^\circ\)C في القارّة القطبيّة الجنوبيّة.",
    "add-sub": r"قديمًا كان التجّار في الصين يكتبون الأرباح بالأحمر والديون بالأسود، أي عكس ما يفعل المحاسبون اليوم!",
    "lines-circles": r"الدائرة هي الشكل الذي يحيط بأكبر مساحة لطول حدود معيّن، لذلك تبني الطيور أعشاشها دائريّة.",
    "angles": r"خلايا النحل سداسيّة، وكل زاوية فيها \(120^\circ\)، وهذا الشكل يوفّر الشمع ويخزّن أكبر كميّة من العسل.",
    "triangles": r"المثلّث لا يتشوّه عند الضغط، لذلك نراه في الجسور وأبراج الكهرباء وسقوف البيوت.",
    "areas": r"مساحة لبنان نحو \(10\,452\ \text{km}^2\)، أي ما يعادل أكثر من مليون ملعب كرة قدم!",
    "ratio": r"نسبة الماء في جسم الإنسان نحو \(\frac{3}{5}\)، أي 60% تقريبًا.",
    "literal": r"كلمة «جبر» عربيّة، جاءت من كتاب الخوارزمي «المختصر في حساب الجبر والمقابلة»، وكلمة «خوارزميّة» جاءت من اسمه.",
    "percent": r"علامة % تطوّرت من الاختصار الإيطاليّ «per cento» أي «لكلّ مئة».",
    "proportional": r"في خريطة مقياسها \(1:100\,000\)، كل 1 cm يمثّل 1 km على الأرض.",
    "stats": r"أوّل إحصاء للسكّان في التاريخ جرى قبل آلاف السنين في بلاد ما بين النهرين ومصر، لتنظيم الزراعة والضرائب.",
}


def fact_box(L):
    f = FACTS.get(L["id"])
    if not f:
        return ""
    return f'''<aside class="fact">{owl(64)}<div class="fact-b"><b>هل تعلم؟</b><p>{f}</p><small>— {MASCOT_NAME}، رفيقك في هذا الكتاب</small></div></aside>'''


def badge(L):
    return f'''<aside class="badge-end">
  <div class="medal"><svg viewBox="0 0 100 100" aria-hidden="true"><path class="rib" d="M30 58 L22 96 L38 86 L48 98 L52 60 Z M70 58 L78 96 L62 86 L52 98 L48 60 Z"/>
    <circle class="med" cx="50" cy="42" r="32"/><circle class="med-in" cx="50" cy="42" r="24"/>
    <text x="50" y="51" text-anchor="middle" class="med-n">{L["num"]}</text></svg></div>
  <div><h4>أحسنت! أنهيت الدرس {L["num"]}</h4><p>لوّن النجوم بحسب إتقانك، ثم انتقل إلى خريطة رحلتي في أوّل الكتاب ولوّن محطّة هذا الدرس.</p>
    <p class="stars"><span>☆</span><span>☆</span><span>☆</span></p></div>
  {owl(70, "owl-cheer")}
</aside>'''


# ---- front matter ------------------------------------------------------------------
def title_page(mk):
    return f'''
<section class="sheet titlepage" id="titlepage">
  <div class="tp-in">
    <p class="tp-eyebrow">{mk("titlepage")}سلسلة «رياضيّاتي» · الصفّ السادس الأساسيّ</p>
    <h1>رياضيات<br><span>الصفّ السادس</span></h1>
    <p class="tp-sub">كتاب التلميذ · وفق الخطّة التعليميّة 2026–2027</p>
    <div class="tp-owl">{owl(150)}<p>أنا <b>{MASCOT_NAME}</b>، سأرافقك في كل درس بمعلومة مدهشة وتشجيع!</p></div>
    <div class="tp-auth"><span>تأليف وإعداد</span><b>حسين زعرور</b><b>محمد عبدالله</b></div>
  </div>
  <div class="tp-legal">
    <p><b>جميع الحقوق محفوظة للمؤلّفَين © 2026.</b> لا يجوز نسخ أيّ جزء من هذا الكتاب أو تصويره أو نشره إلكترونيًّا بأيّ وسيلة دون إذن خطّيّ مسبق من المؤلّفَين.</p>
    <p>الطبعة الأولى: 2026 · ISBN: ______________ · رقم الإيداع: ______________</p>
    <p>للتواصل والطلبات: ______________________________</p>
  </div>
</section>'''


def howto_page(mk, icon):
    items = [("book", "تمهيد وشرح", "موقف من الحياة، ثم شرح واضح وبطاقات قواعد."),
             ("bulb", "ببساطة", "الفكرة بكلمات سهلة، خطوة بخطوة، وحيلة للتذكّر."),
             ("check", "أمثلة محلولة", "حلول مفصّلة مع رسوم دقيقة."),
             ("hat", "تطبيقات وأنشطة", "الرياضيّات في المطبخ والملعب والدكّان."),
             ("pen", "تمارين متدرّجة", "سهل ← متوسّط ← صعب ← تحدٍّ ★، ومهامّ متمايزة."),
             ("target", "بناء المهارات", "خطوات حلّ المسألة: أفهم، أخطّط، أنفّذ، أتحقّق."),
             ("heart", "تعلّم اجتماعيّ عاطفيّ", "تعاون، تأمّل، وعي بالذات، قرار مسؤول."),
             ("compass", "امتحان الدرس", "نموذج امتحان مع حلّه، ثم وسام الإنجاز.")]
    cards = "".join(f'<div class="ht-card"><span class="ico">{icon[i]}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)
    return f'''
<section class="sheet howto6" id="howto">
  <p class="eyebrow">{mk("howto")}دليل الاستخدام</p>
  <h2 class="h-big">كيف تستعمل كتابك؟</h2>
  <div class="ht-hello">{owl(96)}<p>مرحبًا! أنا <b>{MASCOT_NAME}</b>. في كل درس ستجدني في مربّع <b>«هل تعلم؟»</b>. هذه خريطة الكتاب:</p></div>
  <div class="ht-grid">{cards}</div>
  <div class="ht-levels"><span class="lv lv1">سهل</span><span class="lv lv2">متوسّط</span><span class="lv lv3">صعب</span><span class="lv lv4">تحدٍّ ★</span>
    <p>كل الأعداد مكتوبة بالأرقام الإنكليزيّة (0 1 2 3…) والمتغيّرات بالحروف \\(x\\) و\\(y\\).</p></div>
</section>'''


def journey(mk, units, lessons):
    stops = []
    for U in units:
        ls = [L for L in lessons if L["id"] in U["lessons"]]
        dots = "".join(f'<li><span class="j-dot">{L["num"]}</span><small>{L["title"]}</small><i>☆ ☆ ☆</i></li>' for L in ls)
        stops.append(f'<div class="j-unit c-{U["color"]}"><h3><span>{U["num"]}</span>{U["title"]}</h3><ol>{dots}</ol></div>')
    return f'''
<section class="sheet journey" id="journey">
  <p class="eyebrow">{mk("journey")}خريطة رحلتي</p>
  <h2 class="h-big">رحلتي في رياضيّات الصفّ السادس</h2>
  <p class="prose-p">بعد كل درس لوّن نجومه: ★ فهمت · ★★ أتقنت · ★★★ أستطيع أن أشرح لزميلي. وعندما تكمل الرحلة تنتظرك <b>شهادة التفوّق</b> في آخر الكتاب!</p>
  <div class="j-map">{"".join(stops)}</div>
  <div class="j-end">{owl(80, "owl-cheer")}<p>اسمي: ....................................... · صفّي: ............ · بدأتُ الرحلة في: ......./......./.......</p></div>
</section>'''


def certificate(mk):
    return f'''
<section class="sheet cert" id="certificate">
  <div class="cert-in">
    <p class="cert-top">{mk("certificate")}سلسلة «رياضيّاتي» · الصفّ السادس</p>
    <h2>شهادة تفوّق</h2>
    <p class="cert-line">تُمنح هذه الشهادة للتلميذ/ة: <span></span></p>
    <p>لإتمامه رحلة رياضيّات الصفّ السادس بنجاح، وإتقانه دروسها الواحد والعشرين بجدّ ومثابرة.</p>
    <div class="cert-owl">{owl(120, "owl-cheer")}</div>
    <div class="cert-sign"><div><span></span>المعلّم/ة</div><div><span></span>وليّ الأمر</div><div><span></span>التاريخ</div></div>
  </div>
</section>'''


def back_cover(lessons_n, answers_n):
    feats = ["21 درسًا وفق الخطّة التعليميّة 2026–2027", "شرح مبسّط مع «ببساطة» في كل درس", "رسوم دقيقة في الأمثلة والتمارين",
             "تمارين متدرّجة ومهامّ متمايزة", "بناء المهارات والتعلّم الاجتماعيّ العاطفيّ", "8 امتحانات و84 بطاقة مراجعة",
             f"أكثر من {answers_n} إجابة مدقّقة في دليل المعلّم"]
    lis = "".join(f"<li>{f}</li>" for f in feats)
    return f'''
<section class="sheet cover back" id="back">
  <div class="back-in">
    <div class="back-owl">{owl(130)}</div>
    <h2>رياضيّات ممتعة… خطوة بخطوة</h2>
    <p class="back-blurb">كتاب يرافق تلميذ الصفّ السادس في رحلة من الأعداد الكبيرة إلى الهندسة والإحصاء: يشرح ببساطة، يرسم بدقّة،
      ويدرّب بتنوّع، ويبني مهارات الحياة إلى جانب المعرفة الرياضيّة.</p>
    <ul class="back-feats">{lis}</ul>
    <div class="back-auth"><span>تأليف وإعداد</span><b>حسين زعرور · محمد عبدالله</b></div>
    <div class="back-code"><span>ISBN</span><i></i></div>
  </div>
</section>'''
