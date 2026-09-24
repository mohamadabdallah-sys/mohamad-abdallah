# -*- coding: utf-8 -*-
"""Build the Arabic math book: verify answers -> HTML with TeX -> render.js (KaTeX + fonts inline)."""
import base64, json, os, re, subprocess, sys, urllib.request
from content import LESSONS, EXAMS, UNITS, DIAG
import verify
from illustrations import FIGS
from qfigs import render as qfig

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES_FILE = os.path.join(HERE, "pages.json")
PAGES = json.load(open(PAGES_FILE)) if os.path.exists(PAGES_FILE) else {}
PARTS = ["تمهيد", "الشرح", "أمثلة محلولة", "تطبيقات من الحياة", "أنشطة ووسائل تعليميّة", "تمارين",
         "مهامّ متمايزة حسب المستوى", "بناء المهارات: خطوات حلّ المسألة", "صح أم خطأ؟", "تقييم إضافي",
         "التعلّم الاجتماعي العاطفي", "سؤال بحث", "نموذج امتحان الدرس مع الحلّ"]


PART_EMO = {1: "📖", 2: "✍️", 3: "👨‍🍳", 4: "📝", 5: "🧩", 6: "✅", 7: "🎯", 8: "🤝", 9: "🔍", 10: "🏆"}
LESSON_EMO = {"expand": "🔓", "factor": "🧱", "poly": "📈", "roots": "🌱", "rational": "⚖️", "systems": "🔗"}
LEVEL_EMO = {1: "🟢", 2: "🟡", 3: "🔴", 4: "⭐"}
SEL_EMO = {"coop": "🤝", "reflect": "🪞", "self": "🧭", "comm": "💬", "decide": "⚖️", "social": "🌍"}


def emo(e):
    return ""


def stk(e, cls=""):
    """A large decorative emoji 'sticker' placed beside a question or in empty space."""
    return ""


def mk(key):
    """Invisible print marker; make_pdf.py finds it in the PDF to learn the section's page."""
    return f'<em class="pgmark">@@{key}@@</em>'


def pg(key):
    return str(PAGES.get(key, "—"))

INSTR = {
    "powers": "احسب أو اكتب على شكل قوّة:", "primes": "حلّل إلى عوامل أوّليّة، أو احسب:", "fractions": "اختزل أو احسب ثم اختزل:",
    "decimals": "حوّل أو قرّب أو احسب:", "signed-add": "احسب:", "signed-mul": "احسب:", "plane": "أجب عن الأسئلة في مَعلَم متعامد:",
    "algebra": "اختزل أو وسّع أو حلّل:", "equations": "حلّ المعادلات والمسائل:", "proportion": "أجب عن الأسئلة التالية:",
    "triangles": "أجب عن الأسئلة التالية:", "angles": "أجب عن الأسئلة التالية:", "bisectors": "أجب عن الأسئلة التالية:",
}
KIND = {"powers": "احسب", "primes": "حلّل", "fractions": "اختزل / احسب", "decimals": "احسب", "signed-add": "احسب", "signed-mul": "احسب",
        "plane": "مَعلَم", "algebra": "اختزل / وسّع / حلّل", "equations": "حلّ", "proportion": "تناسب", "triangles": "مثلّثات",
        "angles": "زوايا", "bisectors": "منصّفات"}
LEVELS = [("easy", 1, "سهل", "تمارين مباشرة على القاعدة"),
          ("medium", 2, "متوسّط", "قاعدتان أو أكثر في التمرين"),
          ("hard", 3, "صعب", "مستوى الامتحان الرسمي وما فوق"),
          ("challenge", 4, "تحدٍّ", "للمتفوّقين — فكّر خارج الصندوق")]
AR_LETTERS = ["أ", "ب", "ج", "د"]
ROMAN = ["I", "II", "III", "IV", "V"]


def m(t):  return r"\(" + t + r"\)"
def dm(t): return r"\[" + t + r"\]"
def fml(f):  # a rule formula: display TeX, or Arabic HTML when prefixed with "html:"
    return f'<p class="rule-p">{f[5:]}</p>' if f.startswith("html:") else dm(f)


# ---------- icons (inline svg, stroke uses currentColor) ----------------
ICON = {
    "hat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 14.5V19h12v-4.5M6 14.5a4 4 0 0 1-.8-7.9A5 5 0 0 1 12 3.5a5 5 0 0 1 6.8 3.1 4 4 0 0 1-.8 7.9M6 14.5h12M9 16.5v2.5M12 16.5v2.5M15 16.5v2.5"/></svg>',
    "warn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4 2.8 19.5h18.4L12 4zM12 10v4.5M12 17.2v.3"/></svg>',
    "book": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2 2 0 0 1 6 3.5h13v15H6a2 2 0 0 0-2 2zM4 20.5V5.5M8 7.5h7"/></svg>',
    "target": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".6"/></svg>',
    "pen": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.5 4.5l4 4L8 20H4v-4zM13.5 6.5l4 4"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/></svg>',
    "users": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8.5" cy="8" r="3"/><circle cx="16.5" cy="9" r="2.5"/><path d="M3 19c.5-3.3 2.7-5 5.5-5s5 1.7 5.5 5M14.5 14.2c2.9-.4 5.6 1 6.2 4.8"/></svg>',
    "mirror": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a5 5 0 0 1 5 5c0 2.6-1.6 4-2.8 5.2-.7.7-.7 1.4-.7 2.3h-3c0-.9 0-1.6-.7-2.3C8.6 12 7 10.6 7 8a5 5 0 0 1 5-5zM10.5 18.5h3M11 21h2"/></svg>',
    "compass": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5h16v10H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v16M7 20h10M5 7h14M5 7l-2.5 6a2.5 2.5 0 0 0 5 0zM19 7l-2.5 6a2.5 2.5 0 0 0 5 0z"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.6 5.4 3.6 8.5s-1.1 5.9-3.6 8.5c-2.5-2.6-3.6-5.4-3.6-8.5S9.5 6.1 12 3.5z"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V16h5v-.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/></svg>',
}


def meter(n):
    if n == 4:
        return '<span class="meter star" aria-label="تحدٍّ">★</span>'
    return '<span class="meter" aria-label="المستوى %d من 3">%s</span>' % (
        n, "".join('<i class="%s"></i>' % ("on" if k < n else "") for k in range(3)))


def ps_logo():
    data = open(os.path.join(HERE, "assets", "problem-solving.png"), "rb").read()
    return "data:image/png;base64," + base64.b64encode(data).decode()


def logo():
    data = open(os.path.join(HERE, "assets", "book-logo.svg"), "rb").read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


# ---------- sections ----------------------------------------------------
def cover():
    chips = "".join('<li class="c-%s"><b>%d</b>%s</li>' % (L["color"], L["num"], L["title"]) for L in LESSONS)
    glyphs = [r"2^{10}", r"\frac34", r"(-5)+8", r"A(2;3)", r"x+3=7", r"\widehat{ABC}", r"84=2^2\times3\times7",
              r"0.375", r"15\%", r"3x+5", r"a^n", r"\frac{a}{b}"]
    g = "".join('<span class="g g%d">%s</span>' % (i, m(t)) for i, t in enumerate(glyphs))
    return f'''
<section class="sheet cover" id="top">
  <div class="cover-top">
    <div class="cover-logo">{open(os.path.join(HERE, "assets", "book-logo.svg"), encoding="utf-8").read()}</div>
    <p class="cover-eyebrow">الصفّ السابع الأساسيّ · العام الدراسيّ 2026–2027</p>
  </div>
  <svg class="cover-wave" viewBox="0 0 800 70" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 40 C 180 0, 330 70, 520 34 S 720 10, 800 30 L800 70 L0 70 Z" fill="#E9B44C"/>
    <path d="M0 50 C 180 10, 330 80, 520 44 S 720 20, 800 40 L800 70 L0 70 Z" fill="#1B3A7A"/>
  </svg>
  <div class="cover-in">
    <div class="cover-glyphs" aria-hidden="true">{g}</div>
    <h1>رياضيات<br><span>الصفّ السابع</span></h1>
    <div class="authors"><span>إعداد المعلّمَين</span><p>حسين زعرور <i>·</i> محمد عبدالله</p><small dir="ltr">Teachers: Houssein Zaaror &amp; Mohamad Abdallah</small></div>
    <div class="cover-foot">
      <span>الأعداد</span><span>الأعداد النسبيّة والمَعلَم</span><span>الجبر والتناسب</span><span>الهندسة</span>
    </div>
  </div>
</section>'''


def howto():
    rows = "".join(f'<li>{meter(n)}<b>{name}</b><span>{d}</span></li>' for _, n, name, d in LEVELS)
    parts = [("book", "الشرح والقواعد", "فكرة الدرس بكلمات بسيطة، ثم بطاقات القواعد التي يجب حفظها."),
             ("check", "أمثلة محلولة", "حلول خطوة بخطوة — كثير منها من الامتحانات الرسميّة نفسها."),
             ("hat", "تطبيقات", "مسائل من عالم المطبخ والمطعم والحلويات تُظهر فائدة الدرس."),
             ("pen", "تمارين متدرّجة", "من السهل إلى الصعب ثم «تحدٍّ ★» للمتفوّقين."),
             ("heart", "التعلّم الاجتماعي العاطفي", "أنشطة للتعاون والتأمّل والوعي بالذات وإدارتها في كل درس."),
             ("bulb", "بناء المهارات", "أربع خطوات لحلّ أيّ مسألة: أفهم، أخطّط، أنفّذ، أتحقّق."),
             ("check", "تقييم إضافي", "أسئلة اختيار من متعدّد وسؤال مفتوح للتأكّد من الفهم."),
             ("book", "سؤال بحث", "مشروع بحثيّ صغير في كل درس يربط الرياضيّات بالتاريخ والحياة."),
             ("warn", "صح أم خطأ؟", "اصطد الأخطاء الشائعة قبل أن تقع فيها في الامتحان."),
             ("check", "بطاقات MCQ", "36 بطاقة مراجعة للقصّ، الجواب مقلوب في أسفل كل بطاقة."),
             ("pen", "نموذج امتحان الدرس", "امتحان قصير (20 علامة) في نهاية كل درس، يليه الحلّ المفصّل."),
             ("target", "قيّم نفسك", "جدول صغير في آخر كل درس لتعرف ما أتقنتَه وما تحتاج إلى تمرينه.")]
    cards = "".join(f'<div class="how-card"><span class="ico">{ICON[i]}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in parts)
    toc = "".join(f'''<li class="c-{L["color"]}"><a href="#{L["id"]}"><span class="toc-n">{L["num"]}</span>
      <span class="toc-t">{L["title"]}<small dir="ltr">{L["en"].split(" · ")[0]}</small></span></a></li>''' for L in LESSONS)
    toc += '''<li class="c-ink"><a href="#exams"><span class="toc-n">7</span><span class="toc-t">الامتحانات الرسميّة ونماذج<small dir="ltr">Official exams 2015 · 2016 · 2017</small></span></a></li>
      <li class="c-ink"><a href="#summary"><span class="toc-n">8</span><span class="toc-t">بطاقة المراجعة السريعة<small dir="ltr">Formula sheet</small></span></a></li>'''
    return f'''
<section class="sheet front">
  <div class="front-grid">
    <div>
      <p class="credit">إعداد المعلّمَين: <b>حسين زعرور</b> و<b>محمد عبدالله</b></p>
      <h2 class="h-sec">{mk("howto")}كيف تستعمل هذا الكتاب؟</h2>
      <div class="how">{cards}</div>
    </div>
    <div>
      <h3 class="h-sub">مستويات التمارين</h3>
      <ul class="levels">{rows}</ul>
      <p class="note-small">كل الأعداد مكتوبة بالأرقام الإنكليزيّة (0 1 2 3 …) والمتغيّرات بالرمزين \\(x\\) و\\(y\\) كما في النسخة الإنكليزيّة/الفرنسيّة من الامتحان.</p>
    </div>
  </div>
</section>'''


def cards():
    out = []
    k = 0
    for L in LESSONS:
        for q in L["cards"]:
            k += 1
            opts = "".join(f'<li><i>{AR_LETTERS[j]}</i>{(o[5:] if o.startswith("html:") else m(o))}</li>' for j, o in enumerate(q["opts"]))
            out.append(f'''<article class="card c-{L["color"]}">
  <header><span>الدرس {L["num"]}</span><b>{k}</b></header>
  <p class="card-q">{q["q"]}</p>
  <ol class="card-o">{opts}</ol>
  <footer><span class="flip">الجواب: {AR_LETTERS[q["ans"]]})</span></footer>
</article>''')
    return f'''
<section class="sheet cards" id="cards">
  <p class="eyebrow">{mk("cards")}MCQ Cards</p>
  <h2 class="h-big">بطاقات المراجعة: اختيار من متعدّد</h2>
  <p class="prose-p">قُصّ البطاقات على الخطّ المتقطّع، واختبر نفسك أو زميلك. الجواب مكتوب مقلوبًا في أسفل كل بطاقة: اقلب البطاقة بعد أن تختار. (4 بطاقات لكل درس.)</p>
  <div class="card-grid">{"".join(out)}</div>
</section>'''


SHORT = ["تمهيد", "الشرح", "أمثلة", "تطبيقات", "أنشطة", "تمارين", "مستويات", "مهارات", "صح/خطأ", "تقييم", "عاطفيّ", "بحث", "امتحان"]


def index_page():
    def row(href, title, page, cls="", num=""):
        n = f'<span class="toc-n">{num}</span>' if num else ""
        return f'<a class="ix-row {cls}" href="#{href}">{n}<span class="ix-t">{title}</span><i></i><b>{page}</b></a>'
    units = []
    for U in UNITS:
        les = "".join(row(L["id"], L["title"], pg(L["id"]), "ix-les", L["num"])
                      for L in LESSONS if L["id"] in U["lessons"])
        units.append(f'''<div class="ix-unit c-{U["color"]}">
  <a class="ix-uh" href="#unit-{U["num"]}"><span class="ix-un">{U["num"]}</span><span class="ix-t">المحور {U["num"]}: {U["title"]}</span><small dir="ltr">{U["en"]}</small><i></i><b>{pg("unit-" + str(U["num"]))}</b></a>
  {les}</div>''')
    ex = "".join(row(X["id"], X["title"], pg(X["id"]), "ix-sub") for X in EXAMS)
    back = f'''<div class="ix-unit c-ink">
  {row("cards", "بطاقات المراجعة MCQ", pg("cards"), "ix-main")}
  {row("exams", "نماذج الامتحانات", pg("exams"), "ix-main")}
  <div class="ix-ex">{ex}</div>
  {row("summary", "بطاقة المراجعة السريعة", pg("summary"), "ix-main")}</div>'''
    head = "".join(f"<th><span>{p}</span></th>" for p in SHORT)
    trs = []
    for U in UNITS:
        trs.append(f'<tr class="ix-tu c-{U["color"]}"><td colspan="{len(SHORT) + 1}">المحور {U["num"]}: {U["title"]}</td></tr>')
        for L in [L_ for L_ in LESSONS if L_["id"] in U["lessons"]]:
            cells = "".join(f'<td><a href="#{L["id"]}">{pg(L["id"] + "-" + str(i + 1))}</a></td>' for i in range(len(PARTS)))
            trs.append(f'<tr class="c-{U["color"]}"><th class="ix-ln"><a href="#{L["id"]}"><span class="toc-n">{L["num"]}</span>{L["title"]}</a></th>{cells}</tr>')
    return f'''
<section class="sheet index g7-index" id="index">
  <p class="eyebrow">{mk("index")}Contents</p>
  <h2 class="h-big">الفهرس</h2>
  <div class="ix-unit c-ink">{row("diag", "مراجعة واختبار تشخيصيّ (ردم الفجوات)", pg("diag"), "ix-main")}</div>
  {"".join(units)}
  {back}
  <h2 class="h-big ix-h-tab">دليل أقسام الدروس</h2>
  <p class="ix-note">رقم الصفحة التي يبدأ فيها كلّ قسم من أقسام الدرس.</p>
  <div class="ix-scroll"><table class="ix-tab"><thead><tr><th class="ix-ln">الدرس</th>{head}</tr></thead>
  <tbody>{"".join(trs)}</tbody></table></div>
</section>'''


def unit_page(U):
    les = [L for L in LESSONS if L["id"] in U["lessons"]]
    lrows = "".join(f'<li><span class="toc-n">{L["num"]}</span><b>{L["title"]}</b><small dir="ltr">{L["en"].split(" · ")[0]}</small></li>' for L in les)
    qs = "".join(f"<li>{q}</li>" for q in U["questions"])
    return f'''
<section class="sheet unit c-{U["color"]}" id="unit-{U["num"]}">
  <header class="unit-h">{mk("unit-" + str(U["num"]))}
    <p class="eyebrow">المحور التعليميّ {U["num"]}</p>
    <h2>{U["title"]}</h2><p class="op-en" dir="ltr">Unit {U["num"]} · {U["en"]}</p>
  </header>
  <div class="unit-grid">
    <div class="unit-card"><h3>دروس المحور</h3><ol class="unit-lessons">{lrows}</ol>
      <p class="unit-meta"><b>{U["sessions"]} حصّة</b> · {U["period"]}</p></div>
    <div class="unit-card"><h3>الأسئلة الأساسيّة</h3><ul class="unit-q">{qs}</ul></div>
    <div class="unit-card unit-sel"><h3>التعلّم الاجتماعيّ العاطفيّ</h3><p>{U["sel"]}</p></div>
    <div class="unit-card unit-skill"><span class="skb" role="img" aria-label="Problem Solving"></span><div><h3>برنامج بناء المهارات (Skills Builder)</h3>
      <p><b>{U["skill"]}</b> — {U["step"]}</p><p class="unit-act">نشاط المحور: {U["activity"]}</p></div></div>
  </div>
</section>'''


def diag_page():
    parts = []
    k = 0
    for title, items in DIAG["parts"]:
        lis = []
        for q, _, _ in items:
            k += 1
            lis.append(f'<li><span class="q-n">{k}</span><p>{q[5:] if q.startswith("html:") else m(q)}</p><i></i></li>')
        parts.append(f'<div class="diag-part"><h3>{title}</h3><ol>{"".join(lis)}</ol></div>')
    return f'''
<section class="sheet diag c-ink" id="diag">
  <p class="eyebrow">{mk("diag")}المحور الأوّل من الخطّة: ردم الفجوات</p>
  <h2 class="h-big">مراجعة واختبار تشخيصيّ</h2>
  <p class="prose-p">قبل أن نبدأ، لنتأكّد من أنّ الأساس متين: 12 سؤالًا في ثلاثة محاور للمراجعة ({DIAG["sessions"]} حصّة، {DIAG["period"]}).
  أجب بصدق دون مساعدة، فهذا الاختبار ليس للعلامة بل ليعرف المعلّم كيف يساعدك.</p>
  <div class="diag-grid">{"".join(parts)}</div>
</section>'''


def rules_block(L):
    cards = "".join(f'<div class="rule"><span class="rule-k">{k}</span><div class="rule-f">{fml(f)}</div></div>'
                    for k, f in L["rules"])
    return f'<div class="rules">{cards}</div>'


def squares_table():
    cells = "".join('<div><b>%s</b><span>%d</span></div>' % (m(r"\sqrt{%d}" % (n * n)), n) for n in range(1, 16))
    return f'''<div class="squares"><p class="squares-t">المربّعات الكاملة — احفظها!</p><div class="sq-grid" dir="ltr">{cells}</div></div>'''


def example_card(i, ex):
    tag = f'<span class="tag">{ex["tag"]}</span>' if ex.get("tag") else ""
    steps = "".join(f'''<li><div class="st-m">{dm(t)}</div>{f'<p class="st-n">{n}</p>' if n else ""}</li>'''
                    for t, n in ex["steps"])
    return f'''<article class="ex">
  <header><span class="ex-n">مثال {i}</span>{tag}</header>
  <div class="ex-q">{dm(ex["q"])}{f"[[fig:{ex['fig']}]]" if ex.get("fig") else ""}</div>
  <ol class="steps">{steps}</ol>
</article>'''


def app_card(a):
    return f'''<article class="app">
  <header><span class="ico">{ICON["hat"]}</span><h4>{a["title"]}</h4></header>
  <p>{a["body"]}</p>
  <div class="app-sol"><span>الحلّ</span><p>{a["sol"]}</p></div>
</article>'''


def exercises(L):
    out, k = [], 0
    for key, n, name, desc in LEVELS:
        items = []
        for ex in L.get(key, []):
            k += 1
            wide = ex["text"] or L["id"] == "poly"
            body = f'<p>{ex["q"]}</p>' if ex["text"] else dm(ex["q"])
            kind = ex.get("kind") or ("مسألة" if ex["text"] else KIND[L["id"]])
            vary = " vary" if ex.get("kind") else ""
            face = {"اكتشف الخطأ": "🧐", "فسّر": "🤔", "أنشئ": "💡", "سؤال عكسيّ": "🤔"}.get(kind, "")
            items.append(f'<li class="{"wide" if wide else ""}{vary}"><span class="q-n">{k}</span><div class="q-b"><span class="q-kind">{kind}</span>{body}</div>{stk(face, "mini") if face else ""}</li>')
        if not L.get(key):
            continue
        sticker = stk("🤔") if n == 4 else ""
        out.append(f'''<div class="lvl lvl-{n}">{sticker}
  <div class="lvl-h">{meter(n)}<h4>المستوى {n} · {name}</h4><span>{desc}</span></div>
  <ol class="qs">{"".join(items)}</ol>
</div>''')
    return "".join(out)


SKB = '<span class="skb" role="img" aria-label="Problem Solving · حلّ المشكلات"></span>'

STEPS = [("أفهم المسألة", "Understand"), ("أخطّط للحلّ", "Plan"), ("أنفّذ", "Solve"), ("أتحقّق", "Check")]
PROMPTS = ["ما المعطى؟ ما المطلوب؟", "ما القاعدة أو المعادلة التي سأستعملها؟", "أكتب الحلّ خطوة بخطوة:", "هل الجواب منطقيّ؟ أعوّض وأتحقّق:"]


def skills(L):
    sk = L["skills"]
    strip = "".join(f'<li><b>{i + 1}</b><span>{a}</span><small dir="ltr">{e}</small></li>' for i, (a, e) in enumerate(STEPS))
    model = "".join(f'<li><span class="sk-k"><b>{i + 1}</b>{STEPS[i][0]}</span><p>{t}</p></li>'
                    for i, t in enumerate(sk["model"]["steps"]))
    prac = "".join(f'''<article class="sk-p">{stk("🤔", "bottom")}{SKB}<header><span class="q-n">{i + 1}</span><p>{ex["q"]}</p></header>
      <ol class="sk-lines">{"".join(f'<li><span class="sk-k"><b>{j + 1}</b>{STEPS[j][0]}</span><em>{PROMPTS[j]}</em><i></i></li>' for j in range(4))}</ol>
    </article>''' for i, ex in enumerate(sk["practice"]))
    return f'''<div class="skills">
  <p class="sk-banner"><span>مهارة المحور: <b>{sk["skill"]}</b></span><span>{sk["step"]}</span></p>
  <ol class="sk-strip">{strip}</ol>
  <article class="sk-model"><header>{SKB}<span class="tag">مسألة محلولة</span><p>{sk["model"]["q"]}</p></header><ol class="sk-steps">{model}</ol></article>
  <h4 class="sk-your">دورك الآن: حلّ باتّباع الخطوات الأربع</h4>
  {prac}
</div>'''


SEL_KIND = {"coop": ("users", "تعاون", "Cooperation"), "reflect": ("mirror", "التأمّل والتفكّر", "Reflection"),
            "self": ("compass", "الوعي وإدارة الذات", "Self-awareness & management"), "comm": ("chat", "مهارات التواصل", "Relationship skills"),
            "decide": ("scale", "اتخاذ القرار المسؤول", "Responsible decision-making"), "social": ("globe", "الوعي الاجتماعي", "Social awareness")}


def sel(L):
    cards = []
    for a in L["sel"]:
        ic, name, en = SEL_KIND[a["kind"]]
        scale = ('<div class="sel-scale"><span>أقلّ ثقة</span>' + "".join(f"<i>{k}</i>" for k in range(1, 6)) + '<span>واثق جدًّا</span></div>') if a["scale"] else ""
        lines = '<div class="sel-lines">' + "<i></i>" * a["lines"] + "</div>" if a["lines"] else ""
        face = {"reflect": "🤔", "self": "😌", "coop": "😊"}.get(a["kind"], "")
        cards.append(f'''<article class="sel-card sel-{a["kind"]}">{stk(face, "sm") if face else ""}
  <header><span class="ico">{ICON[ic]}</span><div><span class="sel-k">{name}<small dir="ltr">{en}</small></span><h4>{a["title"]}</h4></div><span class="sel-fmt">{a["fmt"]}</span></header>
  <p>{a["body"]}</p>{scale}{lines}
</article>''')
    return f'<div class="sel-grid">{"".join(cards)}</div>'


def quiz(L):
    qs, sols = [], []
    for qi, (prompt, items) in enumerate(L["quiz"]):
        def qhtml(it):
            return f'<p>{it["q"][5:]}</p>' if it["q"].startswith("html:") else dm(it["q"])
        if len(items) == 1:
            body = f'<div class="eq-one">{qhtml(items[0])}</div>'
        else:
            body = '<ol class="eq-items">' + "".join(f'<li><span>{AR_LETTERS[i]})</span>{qhtml(it)}</li>' for i, it in enumerate(items)) + "</ol>"
        qs.append(f'''<li class="eq"><div class="eq-h"><span class="eq-r">{ROMAN[qi]}</span><b>{prompt}</b><span class="pts">5 pts</span></div>{body}</li>''')
        parts = []
        for i, it in enumerate(items):
            steps = "".join(f'''<li><div class="st-m">{dm(t)}</div>{f'<p class="st-n">{n}</p>' if n else ""}</li>''' for t, n in it["steps"])
            lab = f'<span class="qs-lab">{AR_LETTERS[i]})</span>' if len(items) > 1 else ""
            parts.append(f'<div class="qsol-part">{lab}<ol class="steps">{steps}</ol></div>')
        sols.append(f'''<article class="qsol"><header><span class="eq-r">{ROMAN[qi]}</span><b>{prompt}</b></header>{"".join(parts)}</article>''')
    return f'''<div class="lquiz">
  <header class="exam-h">
    <div><span class="badge">نموذج امتحان</span><h2>امتحان الدرس {L["num"]}: {L["title"]}</h2><p>أجب عن الأسئلة التالية قبل أن تنظر إلى الحلّ.</p></div>
    <dl><div><dt>المدّة</dt><dd>30 دقيقة</dd></div><div><dt>العلامة</dt><dd>20</dd></div><div><dt>المستندات</dt><dd>لا شيء</dd></div></dl>
  </header>
  <ol class="eqs">{"".join(qs)}</ol>
</div>
<div class="lquiz-sol">
  <h3 class="sol-h"><span class="ico">{ICON["check"]}</span>الحلّ المفصّل لنموذج الامتحان</h3>
  {"".join(sols)}
</div>'''


def assess(L):
    items = []
    for i, q in enumerate(L["mcq"]):
        opts = "".join(f'<li><i>{AR_LETTERS[j]}</i>{(o[5:] if o.startswith("html:") else m(o))}</li>' for j, o in enumerate(q["opts"]))
        items.append(f'<li class="mcq-q"><span class="q-n">{i + 1}</span><div><p>{q["q"]}</p><ol class="mcq-o">{opts}</ol></div></li>')
    return f'''<div class="assess">
  <p class="instr">اختر الإجابة الصحيحة وضع دائرة حول حرفها:</p>
  <ol class="mcq">{"".join(items)}</ol>
  <div class="open-q">{stk("🤔")}<span class="tag">سؤال مفتوح</span><p>{L["open"]}</p><div class="sel-lines"><i></i><i></i><i></i></div></div>
</div>'''


def research(L):
    r = L["research"]
    return f'''<aside class="research">{stk("🧐")}<header><span class="ico">{ICON["globe"]}</span><div><span class="rs-k">سؤال بحث</span><h4>{r["title"]}</h4></div></header>
  <p>{r["q"]}</p>
  <dl><div><dt>مصادر مقترحة</dt><dd>مكتبة المدرسة، مقابلة مع صاحب مهنة، موقع تعليميّ موثوق</dd></div><div><dt>المنتَج المطلوب</dt><dd>{r["out"]}</dd></div></dl>
</aside>'''


def intro(L):
    it = L["intro"]
    rec = "".join(f'<li><span class="q-n">{i + 1}</span><p>{q}</p><i></i></li>' for i, (q, _, _) in enumerate(it["recall"]))
    return f'''<div class="intro">
  <article class="intro-hook"><span class="rs-k">موقف للتفكير</span><p>{it["hook"]}</p><div class="sel-lines"><i></i></div></article>
  <article class="intro-recall"><span class="rs-k">ماذا أعرف مسبقًا؟</span><ol>{rec}</ol></article>
  <p class="intro-idea"><b>فكرة الدرس:</b> {it["idea"]}</p>
</div>'''


def activities(L):
    cards = []
    for i, a in enumerate(L["activities"]):
        aids = "".join(f"<li>{x}</li>" for x in a["aids"])
        steps = "".join(f"<li>{x}</li>" for x in a["steps"])
        cards.append(f'''<article class="act">
  <header><span class="act-n">نشاط {i + 1}</span><h4>{a["title"]}</h4></header>
  <div class="act-aids"><span>الوسائل</span><ul>{aids}</ul></div>
  <ol class="act-steps">{steps}</ol>
  <p class="act-goal"><b>الهدف:</b> {a["goal"]}</p>
</article>''')
    return f'<div class="acts">{"".join(cards)}</div>'


DIFF = [("support", 1, "دعم", "لمن يحتاج إلى تثبيت الأساس"), ("core", 2, "أساسيّ", "المستوى المطلوب من الجميع"), ("enrich", 3, "إثراء", "للمتميّزين")]


def differentiation(L):
    cols = []
    for key, n, name, desc in DIFF:
        tasks = "".join(f'<li><span class="q-n">{i + 1}</span><div>{t["q"]}</div></li>' for i, t in enumerate(L["diff"][key]))
        cols.append(f'''<article class="dcol dcol-{n}"><header>{meter(n)}<h4>{name}</h4><small>{desc}</small></header><ol>{tasks}</ol></article>''')
    return f'''<p class="instr">يوزّع المعلّم المهامّ على المجموعات حسب مستوى كلّ طالب، ويستطيع الطالب أن ينتقل إلى المستوى التالي متى أتقن مستواه.</p>
<div class="diff">{"".join(cols)}</div>'''


def tf_items(L):
    return "".join(f'''<li><span class="q-n">{i + 1}</span><p>{t["s"]}</p>
      <span class="tf-box"><i></i>صح</span><span class="tf-box"><i></i>خطأ</span></li>''' for i, t in enumerate(L["tf"]))


def self_rows(L):
    return "".join(f'<tr><td>{s}</td><td><i class="box"></i></td><td><i class="box"></i></td></tr>' for s in L["self"])


def lesson(L):
    counter = iter(range(1, 100))
    html = re.sub(r'(<h3 class="h-part(?: quiz-part)?"><span>)\d+(</span>)', lambda m_: f"{m_.group(1)}{next(counter)}{m_.group(2)}", _lesson(L))
    html = html.replace('<p class="eyebrow">الدرس', f'<p class="eyebrow">{mk(L["id"])}الدرس', 1)
    return re.sub(r'<h3 class="h-part( quiz-part)?"><span>(\d+)</span>',
                  lambda m_: f'<h3 class="h-part{m_.group(1) or ""}">{mk(L["id"] + "-" + m_.group(2))}<span>{m_.group(2)}</span>', html)


def _lesson(L):
    goals = "".join(f"<li>{g}</li>" for g in L["goals"])
    words = "".join(f'<tr><td>{a}</td><td dir="ltr">{e}</td><td dir="ltr">{f}</td></tr>' for a, e, f in L["vocab"])
    exs = "".join(example_card(i + 1, e) for i, e in enumerate(L["examples"]))
    apps = "".join(app_card(a) for a in L["apps"])
    sq = squares_table() if L.get("squares") else ""
    return f'''
<section class="sheet lesson c-{L["color"]}" id="{L["id"]}">
  <header class="opener">
    <div class="op-num" aria-hidden="true">{L["num"]}</div>
    <div class="op-t">
      <p class="eyebrow">الدرس {L["num"]} · المحور {L["unit"]}</p>
      <h2>{L["title"]}</h2>
      <p class="op-en" dir="ltr">{L["en"]}</p>
    </div>
  </header>
  <div class="op-meta">
    <div class="goals"><h3><span class="ico">{ICON["target"]}</span>ماذا ستتعلّم؟</h3><ul>{goals}</ul></div>
    <div class="words"><h3><span class="ico">{ICON["book"]}</span>مصطلحات الدرس</h3>
      <div class="tbl"><table><thead><tr><th>عربي</th><th>English</th><th>Français</th></tr></thead><tbody>{words}</tbody></table></div></div>
  </div>

  <h3 class="h-part"><span>0</span>تمهيد<small dir="ltr">Introduction</small></h3>
  {intro(L)}

  <figure class="lesson-fig">{FIGS[L["fig"]][0]()}<figcaption>{FIGS[L["fig"]][1]}</figcaption></figure>

  <h3 class="h-part"><span>0</span>الشرح</h3>
  <div class="prose">{L["explain"]}</div>
  {rules_block(L)}
  {sq}
  <aside class="warn"><span class="ico">{ICON["warn"]}</span><div><b>انتبه! أخطاء شائعة</b><p>{L["warn"]}</p></div></aside>

  <h3 class="h-part"><span>2</span>أمثلة محلولة</h3>
  <div class="exs">{exs}</div>

  <h3 class="h-part"><span>3</span>تطبيقات من الحياة</h3>
  <div class="apps">{apps}</div>

  <h3 class="h-part"><span>0</span>أنشطة ووسائل تعليميّة<small dir="ltr">Activities &amp; teaching aids</small></h3>
  {activities(L)}

  <h3 class="h-part"><span>4</span>تمارين</h3>
  <p class="instr">{INSTR[L["id"]]}</p>
  {exercises(L)}

  <div class="keep"><h3 class="h-part"><span>0</span>مهامّ متمايزة حسب المستوى<small dir="ltr">Differentiation</small></h3>
  {differentiation(L)}</div>

  <h3 class="h-part"><span>5</span>{SKB}بناء المهارات: خطوات حلّ المسألة<small dir="ltr">Skills Builder · Problem-Solving Steps</small></h3>
  {skills(L)}

  <h3 class="h-part"><span>6</span>صح أم خطأ؟</h3>
  <p class="instr">ضع إشارة ✓ في الخانة المناسبة، وصحّح العبارة الخاطئة.</p>
  <div class="tf-wrap">{stk("🤨")}<ol class="tf">{tf_items(L)}</ol></div>

  <h3 class="h-part"><span>7</span>تقييم إضافي<small dir="ltr">Assessment</small></h3>
  {assess(L)}

  <h3 class="h-part"><span>8</span>التعلّم الاجتماعي العاطفي: أنشطة<small dir="ltr">Social-Emotional Learning · SEL</small></h3>
  {sel(L)}

  <h3 class="h-part"><span>9</span>سؤال بحث<small dir="ltr">Research</small></h3>
  {research(L)}

  <aside class="self">{stk("👏")}<h4><span class="ico">{ICON["check"]}</span>قيّم نفسك قبل أن تنتقل إلى الدرس التالي</h4>
    <table><thead><tr><th></th><th>أتقنتُ</th><th>أحتاج تمرينًا</th></tr></thead><tbody>{self_rows(L)}</tbody></table></aside>

  <h3 class="h-part quiz-part"><span>10</span>نموذج امتحان الدرس مع الحلّ</h3>
  {quiz(L)}
</section>'''


def hx(t):
    """TeX by default; HTML when prefixed with 'html:'."""
    if t.startswith("html:"):
        return t[5:]
    return t if "\\(" in t else m(t)


def exams():
    out = ['''<section class="sheet exams-intro" id="exams">
  <p class="eyebrow">''' + mk("exams") + '''نماذج الامتحانات</p>
  <h2 class="h-big">امتحانات المحاور ونهاية الفصلين</h2>
  <p class="prose-p">أربعة امتحانات، واحد لكل محور (50 دقيقة)، ثم امتحانا نهاية الفصل الأوّل ونهاية العام (ساعة ونصف).
  كل امتحان من أربعة أسئلة، <b>5 علامات لكل سؤال</b>، والآلة الحاسبة <b>غير مسموحة</b>. حلّ كل امتحان في وقته الحقيقيّ ثم اطلب التصحيح من معلّمك.</p>
  <ul class="exam-tips">
    <li><span class="ico">''' + ICON["bulb"] + '''</span><p><b>اقرأ السؤال كاملًا</b> قبل أن تبدأ، وضع خطًّا تحت المطلوب.</p></li>
    <li><span class="ico">''' + ICON["bulb"] + '''</span><p><b>الأولويّات:</b> الأقواس، ثم القوى، ثم الضرب والقسمة، ثم الجمع والطرح.</p></li>
    <li><span class="ico">''' + ICON["bulb"] + '''</span><p><b>تحقّق</b> من حلّ المعادلة بالتعويض، ومن مجموع زوايا المثلّث (\\(180^\\circ\\)).</p></li>
  </ul>
</section>''']
    for X in EXAMS:
        qs = []
        for qi, (ar, en, items) in enumerate(X["qs"]):
            one = lambda t: f'<p class="eq-p">{t[5:]}</p>' if t.startswith("html:") else dm(t)
            if len(items) == 1:
                its = f'<div class="eq-one">{one(items[0][0])}</div>'
            else:
                its = '<ol class="eq-items">' + "".join(f'<li><span>{AR_LETTERS[i]})</span>{one(t)}</li>' for i, (t, _, _) in enumerate(items)) + "</ol>"
            qs.append(f'''<li class="eq"><div class="eq-h"><span class="eq-r">{ROMAN[qi]}</span><b>{ar}</b><small dir="ltr">{en}</small><span class="pts">5 pts</span></div>{its}</li>''')
        final = X["id"].startswith("final")
        out.append(f'''
<section class="sheet exam {"official" if final else "mock"}" id="{X["id"]}">
  <header class="exam-h">
    <div>{mk(X["id"])}<span class="badge">{"نهاية فصل" if final else "امتحان محور"}</span><h2>{X["title"]}</h2><p>{X["sub"]}</p></div>
    <dl><div><dt>المدّة</dt><dd>{X["time"]}</dd></div><div><dt>التوزيع</dt><dd>5 علامات / سؤال</dd></div><div><dt>الآلة الحاسبة</dt><dd>غير مسموحة</dd></div></dl>
  </header>
  <div class="exam-name"><span>الاسم: ............................................</span><span>الصفّ: ...........</span><span>العلامة: ........ / 20</span></div>
  <ol class="eqs">{"".join(qs)}</ol>
</section>''')
    return "".join(out)


def summary():
    blocks = []
    for L in LESSONS:
        r = "".join(f'<li><span class="sum-k">{k}</span>{fml(f)}</li>' for k, f in L["rules"])
        blocks.append(f'<div class="sum c-{L["color"]}"><h3><b>{L["num"]}</b>{L["title"]}</h3><ul>{r}</ul></div>')
    return f'''
<section class="sheet summary" id="summary">
  <p class="eyebrow">{mk("summary")}قبل الامتحان</p>
  <h2 class="h-big">بطاقة المراجعة السريعة</h2>
  <div class="sum-grid">{"".join(blocks)}</div>
</section>'''


def answers():
    out = []
    for L in LESSONS:
        k, items = 0, []
        for key, n, name, _ in LEVELS:
            for ex in L.get(key, []):
                k += 1
                hint = f'<small class="hint">تلميح: {ex["hint"]}</small>' if ex.get("hint") else ""
                items.append(f'<li><span class="a-n">{k}</span><div>{ex["a"] if ex["ahtml"] else m(ex["a"])}{hint}</div></li>')
        sk = "".join(f'<li><span class="a-n">{i + 1}</span><div>{ex["a"]}</div></li>' for i, ex in enumerate(L["skills"]["practice"]))
        rc = "".join(f'<li><span class="a-n">{i + 1}</span><div>{a}</div></li>' for i, (_, a, _) in enumerate(L["intro"]["recall"]))
        df = "".join(f'<li><span class="a-n">{name[0]}{i + 1}</span><div>{t["a"]}</div></li>'
                     for key, _, name, _ in DIFF for i, t in enumerate(L["diff"][key]))
        mc = "".join(f'<li><span class="a-n">{i + 1}</span><div><b>{AR_LETTERS[q["ans"]]})</b></div></li>' for i, q in enumerate(L["mcq"]))
        tf = "".join(f'''<li><span class="a-n">{i + 1}</span><div><b class="{"ok" if t["truth"] else "no"}">{"صح" if t["truth"] else "خطأ"}</b>{(" — " + t["fix"]) if t["fix"] else ""}</div></li>'''
                     for i, t in enumerate(L["tf"]))
        out.append(f'<div class="ans c-{L["color"]}"><h3><b>{L["num"]}</b>{L["title"]}</h3><ol>{"".join(items)}</ol>'
                   f'<p class="ans-sub">تمهيد: ماذا أعرف مسبقًا؟</p><ol>{rc}</ol>'
                   f'<p class="ans-sub">المهامّ المتمايزة (د = دعم، أ = أساسيّ، إ = إثراء)</p><ol>{df}</ol>'
                   f'<p class="ans-sub">بناء المهارات</p><ol>{sk}</ol>'
                   f'<p class="ans-sub">اختيار من متعدّد</p><ol class="ans-mc">{mc}</ol>'
                   f'<p class="ans-sub">صح أم خطأ؟</p><ol>{tf}</ol></div>')
    for X in EXAMS:
        items = []
        for qi, (_, _, its) in enumerate(X["qs"]):
            parts = " &nbsp;·&nbsp; ".join((f"{AR_LETTERS[i]}) " if len(its) > 1 else "") + hx(a) for i, (_, a, _) in enumerate(its))
            items.append(f'<li><span class="a-n">{ROMAN[qi]}</span><div>{parts}</div></li>')
        out.append(f'<div class="ans c-ink" id="ans-{X["id"]}"><h3><b>✓</b>{X["title"]}</h3><ol>{"".join(items)}</ol></div>')
    k, items = 0, []
    for _, its in DIAG["parts"]:
        for _, a, _ in its:
            k += 1
            items.append(f'<li><span class="a-n">{k}</span><div>{hx(a) if a.startswith("html:") else a}</div></li>')
    out.insert(0, f'<div class="ans c-ink"><h3><b>✓</b>الاختبار التشخيصيّ</h3><ol>{"".join(items)}</ol></div>')
    return f'''
<section class="sheet answers" id="answers">
  <p class="eyebrow">للمعلّم فقط</p>
  <h2 class="h-big">دليل الإجابات</h2>
  <p class="prose-p">الإجابات النهائيّة لكل تمارين كتاب «رياضيات الصفّ السابع» (2026–2027) — إعداد المعلّمَين حسين زعرور ومحمد عبدالله.
  الحلول المفصّلة لنماذج امتحانات الدروس موجودة داخل الكتاب.</p>
  <div class="ans-grid">{"".join(out)}</div>
</section>'''


# ---------- fonts: download Google fonts once and inline them ----------
def font_css():
    css = open(os.path.join(HERE, "fonts", "fonts.css"), encoding="utf-8").read()
    blocks = re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face\s*\{.*?\})", css, re.S)
    out, cache = [], {}
    for subset, blk in blocks:
        if subset not in ("arabic", "latin"):
            continue
        url = re.search(r"url\((https://[^)]+)\)", blk).group(1)
        if url not in cache:
            fn = os.path.join(HERE, "fonts", os.path.basename(url))
            if not os.path.exists(fn):
                urllib.request.urlretrieve(url, fn)
            cache[url] = "data:font/woff2;base64," + base64.b64encode(open(fn, "rb").read()).decode()
        out.append(blk.replace(url, cache[url]))
    return "\n".join(out)


def main():
    n, bad = verify.run()
    if bad:
        print("answers failed verification:", bad); sys.exit(1)
    print(f"verified {n} answers")
    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    body = []
    for U in UNITS:
        body.append(unit_page(U))
        body += [lesson(L) for L in LESSONS if L["id"] in U["lessons"]]
    book = cover() + index_page() + diag_page() + "".join(body) + cards() + exams() + summary()
    page(css, "رياضيات الصف السابع", book, "index.html")
    page(css, "دليل الإجابات للمعلم", answers(), "answers.html")


def page(css, title, body, out):
    html = f'''<title>{title}</title>
<meta name="description" content="كتاب رياضيات الصفّ السابع 2026–2027: شرح، أمثلة، أنشطة، بناء المهارات، تعلّم اجتماعيّ عاطفيّ، وتمارين متدرّجة">
<style>
{font_css()}
.skb {{ background-image: url({ps_logo()}); }}
/*KATEX_CSS*/
{css}
</style>
<div class="book" dir="rtl" lang="ar">
{body}
<footer class="colophon">رياضيات الصفّ السابع · 2026–2027 · إعداد المعلّمَين حسين زعرور ومحمد عبدالله</footer>
</div>
'''
    html = re.sub(r"\[\[fig:([\w-]+)\]\]", lambda m_: qfig(m_.group(1)), html)
    src = os.path.join(HERE, "book.src.html")
    open(src, "w", encoding="utf-8").write(html)
    subprocess.run(["node", os.path.join(HERE, "render.js"), src, os.path.join(HERE, out)], check=True)


if __name__ == "__main__":
    main()
