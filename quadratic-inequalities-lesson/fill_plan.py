# Fills the school's daily lesson-plan form (تحضير يومي) for the quadratic inequalities lesson.
# Usage: unzip the school form (DDR-F19 .DOC, really .docx) to a folder, then
#        python3 fill_plan.py <folder>  and zip the folder back.
# The template holds two plan pages; page 1 = session 1, page 2 = session 2.
# Math inside Arabic text is written as {{...}} and gets its own left-to-right run.
import re
import sys
from xml.sax.saxutils import escape

D = sys.argv[1] + "/word/document.xml"
xml = open(D, encoding="utf8").read()

S1 = {
    "date": "التاريخ: ……/……/2027 .              الصف/الشعبة : ………………        عنوان الدرس: المتراجحات من الدرجة الثانية (1/2): إشارة ثلاثي الحدود",
    "goals": [
        "أن يربط التلميذ إشارة ثلاثي الحدود {{f(x) = ax² + bx + c}} بموقع منحنيه بالنسبة لمحور الفواصل.",
        "أن يحدّد التلميذ إشارة ثلاثي الحدود حسب إشارة المميّز Δ وإشارة a.",
    ],
    "terms": "المصطلحات (جديدة-علمية): متراجحة من الدرجة الثانية، ثلاثي الحدود، المميّز Δ، جذر، جدول الإشارة.",
    "styles": "أنماط التعلم / نوع الذكاء المستخدمة: 🖵 لغوي     ✓ رياضي- منطقي     ✓ مكاني – بصري     🖵 حركي - جسدي     🖵 موسيقي - سمعي     ✓ إجتماعي     🖵 ذاتي - نفسي     🖵 طبيعي - بيولوجي",
    "act1": "النشاط 1 (التمهيد): ✓ ربط بالمكتسبات السابقة    🖵 محادثة شفهية    🖵 فيديو    🖵 نشاط استقصائي    🖵 سرد قصة    🖵 خريطة مفاهيم    🖵 مراجعة الدرس السابق    🖵 غير ذلك .      المدة 10 د .",
    "act1_body": "يحلّ التلاميذ فرديًا ثلاثة أسئلة (الشريحة 3): حلّ المعادلة {{x² − 5x + 6 = 0}}، وحساب Δ للمعادلة {{2x² + x + 3 = 0}}، وإكمال جدول إشارة {{2x − 4}}. يليها تصحيح جماعي سريع، ويستفيد المعلم من النتائج لتوزيع التلاميذ على الفئات في الحصة الثانية.",
    "act2": "النشاط 2 ( ذكر مدة النشاط ): مراحل التعلّم: ✓ الإستكشاف ✓ التفسير 🖵 التطبيق/التدريب/التوسيع - المدة : 35 د.",
    "tools": "الوسائل: لوح تفاعلي – عرض PowerPoint – GeoGebra – بطاقة استكشاف",
    "strategy": "الإستراتيجية: استقصاء موجّه / عمل ثنائي",
    "steps": [
        "سير النشاط :",
        "1) استكشاف (10 د): يعرض المعلم منحنى {{f(x) = x² − x − 6}} (الشريحة 4) ويسأل: أين يقطع المنحنى محور الفواصل؟ متى يقع فوقه ومتى يقع تحته؟ يستنتج التلاميذ أنّ {{f(x) < 0}} بين الجذرين −2 و 3، وأنّها موجبة خارجهما.",
        "2) عمل ثنائي (12 د): يدرس كل ثنائي الدوال {{x² − 2x − 3}} و {{x² − 2x + 1}} و {{x² − 2x + 3}} (الشريحة 5): يحسب Δ، ويحدّد عدد نقاط التقاطع مع محور الفواصل، ويصف إشارة الدالة.",
        "3) التفسير (13 د): تعرض الثنائيات نتائجها، ويقود المعلم صياغة القاعدة (الشريحة 6): ثلاثي الحدود يأخذ إشارة a دائمًا، إلا بين الجذرين عندما {{Δ > 0}}. يدوّن التلاميذ جداول الإشارة للحالات الثلاث في دفاترهم.",
    ],
    "diff": "للفروقات الفردية: جدول قيم جاهز للمتعثرين لقراءة المنحنى، وسؤال إضافي للمتفوقين: ماذا يتغيّر إذا كان {{a < 0}}؟",
    "eval": "النشاط التقييمي: ✓أسئلة شفهية    🖵بطاقة تقييم    🖵عمل مجموعات    🖵مناقشة و حوار",
    "eval_body": "يحدّد التلاميذ شفهيًا، ومن دون رسم، إشارة {{x² − 4x + 3}} وإشارة {{−x² + 2x − 5}}.",
    "homework": "ادرس إشارة كلٍّ من {{2x² − 3x − 2}} و {{x² + 6x + 9}}.",
    "support": "بطاقة دعم: جدول إشارة جاهز للتعبئة لثلاثي الحدود {{x² − 9}}.",
    "reflect": "الفقرة التأملية:  تحقق الأهداف بنسبة ……%.",
}

S2 = {
    "date": "التاريخ: ……/……/2027 .              الصف/الشعبة : ………………        عنوان الدرس: المتراجحات من الدرجة الثانية (2/2): حل المتراجحة",
    "goals": [
        "أن يحلّ التلميذ متراجحة من الدرجة الثانية ويكتب مجموعة الحلول على شكل مجال أو اتحاد مجالات.",
        "أن يوظّف التلميذ المتراجحات في حلّ مسألة حياتية.",
    ],
    "terms": "المصطلحات (جديدة-علمية): مجموعة الحلول، مجال مغلق، مجال مفتوح، اتحاد مجالات.",
    "styles": "أنماط التعلم / نوع الذكاء المستخدمة: 🖵 لغوي     ✓ رياضي- منطقي     🖵 مكاني – بصري     🖵 حركي - جسدي     🖵 موسيقي - سمعي     ✓ إجتماعي     🖵 ذاتي - نفسي     🖵 طبيعي - بيولوجي",
    "act1": "النشاط 1 (التمهيد): 🖵 ربط بالمكتسبات السابقة    🖵 محادثة شفهية    🖵 فيديو    🖵 نشاط استقصائي    🖵 سرد قصة    🖵 خريطة مفاهيم    ✓ مراجعة الدرس السابق    🖵 غير ذلك .      المدة 10 د .",
    "act1_body": "يستذكر التلاميذ قاعدة إشارة ثلاثي الحدود عبر سؤال سريع: ما إشارة {{x² − x − 6}}؟ ثم يعرض المعلم خطوات الحل الأربع (الشريحة 7): نرتّب المتراجحة، نحسب Δ والجذور، ننشئ جدول الإشارة، نكتب مجموعة الحلول.",
    "act2": "النشاط 2 ( ذكر مدة النشاط ): مراحل التعلّم: 🖵 الإستكشاف ✓ التفسير ✓ التطبيق/التدريب/التوسيع - المدة : 35 د.",
    "tools": "الوسائل: لوح تفاعلي – عرض PowerPoint – بطاقات الفئات الثلاث",
    "strategy": "الإستراتيجية: نمذجة / عمل مجموعات متعدد المستويات",
    "steps": [
        "سير النشاط :",
        "1) نمذجة (10 د): يحلّ المعلم بصوت مسموع المتراجحة {{x² − x − 6 ≤ 0}} فيحسب المميّز {{Δ = 25}} ويجد الجذرين −2 و 3، ثم ينشئ جدول الإشارة ويستنتج مجموعة الحلول {{S = [−2 ; 3]}}. يعرض بعدها حالتي {{Δ < 0}} و {{Δ = 0}} والأخطاء الشائعة (الشرائح 8–10).",
        "2) تعدد المستويات (15 د): مجموعات من 4 تلاميذ تُشكَّل حسب نتائج تمهيد الحصة الأولى، وتحلّ كل فئة سؤالًا واحدًا:",
        "   الفئة الأولى (أساسي): حلّ في ℝ المتراجحة {{x² − 9 ≤ 0}}",
        "   الفئة الثانية (متوسط): حلّ في ℝ المتراجحة {{3x² ≤ 2x + 1}}",
        "   الفئة الثالثة (متقدّم): مستطيل محيطه 20 سم وطوله x. أوجد قيم x التي تجعل مساحته 21 سم² على الأقل.",
        "الحلول المتوقعة: الفئة الأولى {{S = [−3 ; 3]}} ، الفئة الثانية {{S = [−1/3 ; 1]}} ، الفئة الثالثة نكتب {{x(10 − x) ≥ 21}} فنجد {{x ∈ [3 ; 7]}}.",
        "3) عرض ومناقشة (10 د): تعرض كل فئة حلّها على اللوح، ويصحّح الصف ويربط الحلول الثلاثة بالقاعدة.",
    ],
    "diff": "للفروقات الفردية: سؤال واحد لكل فئة حسب مستواها، وبطاقة مساعدة (جدول إشارة جاهز) للفئة الأولى. من ينهي باكرًا يحلّ سؤال الفئة التالية.",
    "eval": "النشاط التقييمي: 🖵أسئلة شفهية    ✓بطاقة تقييم    ✓عمل مجموعات    🖵مناقشة و حوار",
    "eval_body": "بطاقة خروج (دقيقتان): حلّ في ℝ المتراجحة {{x² − 4 > 0}}.",
    "homework": "حلّ في ℝ المتراجحتين {{−x² + x + 6 > 0}} و {{4x² − 4x + 1 ≤ 0}}.",
    "support": "بطاقة دعم: حلّ المتراجحة {{x² − 16 < 0}} (تمرين مشابه لسؤال الفئة الأولى مع جدول إشارة جاهز).",
    "reflect": "الفقرة التأملية:  تحقق الأهداف بنسبة ……%.",
}

def runs_for(rpr, text):
    """Split text on {{math}} and build runs; each math part becomes a Word equation,
    which always stays left-to-right inside Arabic text."""
    out = []
    for i, part in enumerate(re.split(r"\{\{(.*?)\}\}", text)):
        if not part:
            continue
        if i % 2:  # math, as normal (upright) text in the paragraph's font and colour
            r = re.sub(r'<w:rtl w:val="[01]"/>', "", rpr)
            out.append(f'<m:oMath><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t xml:space="preserve">{escape(part)}</m:t></m:r></m:oMath>')
        else:
            out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def para_text(p):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))


def rebuild(p, text):
    """Keep the paragraph's pPr and its first text run's formatting; replace all runs."""
    ppr = re.search(r"<w:pPr>.*?</w:pPr>", p, re.S)
    first = re.search(r"<w:r>(<w:rPr>.*?</w:rPr>)<w:t", p, re.S)
    rpr = first.group(1) if first else "<w:rPr/>"
    head = p[: p.find(">") + 1]
    return head + (ppr.group(0) if ppr else "") + runs_for(rpr, text) + "</w:p>"


paras = list(re.finditer(r"<w:p [^>]*>.*?</w:p>", xml, re.S))
# locate each plan's paragraphs by their template text (start of text) and occurrence
KEYS = {
    "date": "التاريخ:",
    "goals": "أن ",
    "terms": "المصطلحات",
    "styles": "أنماط التعلم",
    "act1": "النشاط 1",
    "act2": "النشاط 2",
    "tools": "الوسائل:",
    "strategy": "الإستراتيجية:",
    "steps": "سير النشاط",
    "diff": "للفروقات الفردية",
    "eval": "النشاط التقييمي",
    "homework": "الواجب البيتي",
    "support": "بطاقة دعم",
    "reflect": "الفقرة التأملية",
}
found = {k: [] for k in KEYS}
act1_body, eval_body = [], []
for idx, m in enumerate(paras):
    t = para_text(m.group(0)).strip()
    for k, pre in KEYS.items():
        if t.startswith(pre):
            found[k].append(idx)
    if idx > 0 and para_text(paras[idx - 1].group(0)).strip().startswith("النشاط 1"):
        act1_body.append(idx)
    if idx > 0 and para_text(paras[idx - 1].group(0)).strip().startswith("النشاط التقييمي"):
        eval_body.append(idx)
for k, v in found.items():
    assert len(v) == 2, (k, v)
assert len(act1_body) == 2 and len(eval_body) == 2

repl = {}  # paragraph index -> new xml
for n, S in enumerate([S1, S2]):
    def p(k):
        return paras[found[k][n]].group(0)
    for k in ["date", "terms", "styles", "act1", "act2", "tools", "strategy", "diff", "eval", "support", "reflect"]:
        repl[found[k][n]] = rebuild(p(k), S[k])
    repl[act1_body[n]] = rebuild(paras[act1_body[n]].group(0), S["act1_body"])
    repl[eval_body[n]] = rebuild(paras[eval_body[n]].group(0), S["eval_body"])
    repl[found["goals"][n]] = "".join(rebuild(p("goals"), g) for g in S["goals"])
    repl[found["steps"][n]] = "".join(rebuild(p("steps"), s) for s in S["steps"])
    # homework: keep the red heading, add the task below it in the support-card style
    repl[found["homework"][n]] = p("homework") + rebuild(p("support"), S["homework"])

out, last = [], 0
for idx, m in enumerate(paras):
    if idx in repl:
        out.append(xml[last : m.start()])
        out.append(repl[idx])
        last = m.end()
out.append(xml[last:])
xml = "".join(out)
# paragraph ids must stay unique after cloning
seen = set()
def fix_id(m):
    pid = m.group(1)
    if pid in seen:
        pid = format(0x10000000 + len(seen), "08X")
    seen.add(pid)
    return f'w14:paraId="{pid}"'
xml = re.sub(r'w14:paraId="([0-9A-Fa-f]{8})"', fix_id, xml)
# drop the template's blank lines inside the activity cell so each plan stays on two pages
def tidy_cell(m):
    tc = m.group(0)
    if "سير النشاط" not in tc:
        return tc
    return re.sub(r"<w:p [^>]*>(?:(?!</w:p>).)*</w:p>", lambda p: p.group(0) if para_text(p.group(0)).strip() else "", tc, flags=re.S)
xml = re.sub(r"<w:tc>.*?</w:tc>", tidy_cell, xml, flags=re.S)
open(D, "w", encoding="utf8").write(xml)
print("filled")
