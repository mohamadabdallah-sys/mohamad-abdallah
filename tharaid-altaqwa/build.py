# -*- coding: utf-8 -*-
"""Step 2: turn build/edited.txt into the typeset book (build/book.html, paginated by Paged.js).

- every topic starts on a new page, the table of contents comes at the end
- Qur'an quotations are matched in the Mushaf, printed in Uthmani script and referenced in a footnote
- every source (inline brackets, end-of-topic source lists, Word footnotes) becomes a numbered footnote
"""
import html, os, re, sys, unicodedata
from quran import Quran
import ornaments as O
from sources import canon

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)

TITLE = "ثرائد التقوى"
AUTHOR = "محمد عبدالله"
# the final, proofread and vocalised text (made from build/edited.txt); falls back to prep.py's output
TEXT = P("src", "text.txt") if os.path.exists(P("src", "text.txt")) else P("build", "edited.txt")

SURA_FIX = {14: "إبراهيم", 34: "سبأ", 76: "الإنسان", 78: "النبأ", 82: "الانفطار", 84: "الانشقاق"}

SUBHEADS = ("أولاً: الكذب على الله ورسوله", "ثانياً: الكذب على الناس", "أ – الحلف بالزور",
            "ب – الكذب بقصد المزاح والسخرية", "ثالثاً: الكذب على النفس", "الطريق الأول: طريق المعرفة",
            "الطريق الثاني: طريق المجاهدة", "التأمل", "العبرة")

# sources for the numbered references of «أبكي لظلمة قبري» (its source list was missing in the manuscript)
GRAVE_SOURCES = {
    13: "بحار الأنوار، للعلامة المجلسي، ج 6، أبواب الموت وما يلحقه من أحوال البرزخ.",
    14: "الكافي، للشيخ الكليني، ج 3، كتاب الجنائز، باب المسألة في القبر ومن يُسأل ومن لا يُسأل.",
    15: "الصحيفة السجادية، الدعاء الثالث (في الصلاة على حملة العرش وكل ملك مقرّب).",
    16: "الأمالي، للشيخ الطوسي (من كتاب أمير المؤمنين عليه السلام إلى محمد بن أبي بكر).",
    17: "بحار الأنوار، للعلامة المجلسي، ج 79 (وصية السيدة فاطمة الزهراء عليها السلام).",
    19: "معاني الأخبار، للشيخ الصدوق، باب معنى الموت.",
    20: "تصحيح اعتقادات الإمامية، للشيخ المفيد.",
    21: "الأمالي، للشيخ الصدوق؛ ومعاني الأخبار، باب معنى الموت.",
}

SRC_KW = ("الكافي", "نهج البلاغة", "بحار", "وسائل", "مستدرك", "الصحيفة", "عيون", "تحف", "الأمالي", "أمالي",
          "غرر", "ميزان الحكمة", "من لا يحضره", "الخصال", "ثواب الأعمال", "معاني الأخبار", "علل الشرائع",
          "مصباح", "كنز العمال", "مجمع البيان", "تفسير", "الإرشاد", "كمال الدين", "تهذيب", "المحاسن",
          "جامع الأخبار", "مشكاة", "الكنى", "عوالي", "شرح نهج", "التوحيد", "بصائر", "الإثنا عشرية",
          "مكارم", "روضة", "البرهان", "الاستبصار", "دعاء", "رواه", "مخرج", "المصدر", "مناقب",
          "الطبري", "الريشهري", "كشف الغمة")
KW = "|".join(map(re.escape, SRC_KW))

AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
WEST = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

Q = Quran()
NAME2ID = {}


def norm_name(s):
    s = re.sub(r"[ً-ْٰ]", "", s)
    s = re.sub("[أإآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    s = re.sub(r"^سوره\s*", "", s.strip())
    return s.replace(" ", "")


for sid, name in Q.names.items():
    NAME2ID[norm_name(name)] = sid
    if sid in SURA_FIX:
        NAME2ID[norm_name(SURA_FIX[sid])] = sid
        Q.names[sid] = SURA_FIX[sid]
NAME2ID[norm_name("ص")] = 38

report = []


# ----------------------------------------------------------------------------- footnote text
def clean_note(t):
    t = re.sub("[\u064B-\u0652\u0670\u0640]", "", t)
    t = re.sub(r"\^\d+\^", "", t)
    t = t.replace("**", "").replace("_", "")
    t = re.sub(r"^\s*\(?\s*المصدر\s*[:：]\s*", "", t)
    t = re.sub(r"^\s*\(\s*(.*?)\s*\)\s*\.?$", r"\1", t)
    t = t.translate(WEST)
    t = re.sub(r"(?<![\w])(ج|ص|ح)\s*\.?\s*(\d)", r"\1 \2", t)
    t = re.sub(r"\s+", " ", t).strip(" ،,")
    t = t.replace(" -- ", " – ").replace(" - ", " – ")
    t = re.sub(r"\s+([،؛:.])", r"\1", t)
    t = re.sub(r"^القرآن الكريم\s*[،:]\s*", "", t)
    t = re.sub(r"\s*–\s*الشيخ الكليني", "، للشيخ الكليني", t)
    t = re.sub(r"^((?:أصول )?الكافي|نهج البلاغة|الصحيفة السجادية|تفسير القمي|عيون أخبار الرضا(?: \(ع\))?|تحف العقول|"
               r"وسائل الشيعة|مستدرك الوسائل|بحار الأنوار|غرر الحكم|مشكاة الأنوار|عيون الأخبار|المحاسن|كمال الدين|"
               r"ثواب الأعمال|الخصال للصدوق|جامع الأخبار|تحف العقول)\s*:\s*", r"\1، ", t)
    t = re.sub(r"(الحكمة|الخطبة|الكتاب|الحديث|الدعاء)\s*(?:رقم\s*|:\s*)", r"\1 ", t)
    t = re.sub(r"(^|،\s*)(خطبة|حكمة)\s+(?:رقم\s*)?(\d)", lambda m: m.group(1) + "ال" + m.group(2) + " " + m.group(3), t)
    t = re.sub(r"^(الكافي|أصول الكافي)،?\s*(?:الشّيخ|الشيخ|للكليني|للشيخ الكليني|الشيخ الكليني)\b،?", r"\1، للشيخ الكليني،", t)
    t = re.sub(r"^الكافي للشيخ الكليني|^الكافي للكليني", "الكافي، للشيخ الكليني", t)
    t = t.replace("الكافي، كتاب الكافي للشيخ الكليني", "الكافي، للشيخ الكليني")
    t = t.replace("المجلد الثاني", "ج 2").replace("المجلد الثالث", "ج 3").replace("الصفحة ", "ص ")
    t = t.replace("،،", "،").rstrip("،. ")
    t = re.sub(r"(^|،\s*)حكم\s+(\d)", r"\1الحكمة \2", t)
    t = re.sub(r"^قول [^:]{3,40}:\s*\((.*)\)\.?$", r"\1", t)
    t = re.sub(r"ج (\d+)/ص", r"ج \1، ص", t)
    t = honorifics(quotes(t))
    if not t.startswith("سورة"):
        t = canon(t)
    if not t.endswith((".", "»")):
        t += "."
    return t


def quran_note(refs):
    parts = []
    for s1, a1, s2, a2 in refs:
        if s1 != s2:
            parts.append("سورة %s، الآية %d؛ وسورة %s، الآية %d" % (Q.names[s1], a1, Q.names[s2], a2))
        elif a1 == a2:
            parts.append("سورة %s، الآية %d" % (Q.names[s1], a1))
        elif a2 == a1 + 1:
            parts.append("سورة %s، الآيتان %d–%d" % (Q.names[s1], a1, a2))
        else:
            parts.append("سورة %s، الآيات %d–%d" % (Q.names[s1], a1, a2))
    # merge consecutive refs of the same sura (fragments of one passage)
    return "؛ ".join(dict.fromkeys(parts)) + "."


QREF = re.compile(r"""\s*[\[\(]\s*(?:القرآن\sالكريم[،,]?\s*)?(?:سورة\s*)?(?P<name>[^\[\]\(\)\d:،,]{1,20}?)\s*[:،,]\s*
                      (?:الآية|الآيات|الآيتان)?\s*(?:رقم)?\s*(?P<a>[\d٠-٩]+)(?:\s*[-–]\s*(?P<b>[\d٠-٩]*))?\s*\.?\s*[\]\)]\.?""",
                  re.X)


def parse_qref(m):
    sid = NAME2ID.get(norm_name(m.group("name")))
    return sid


# ----------------------------------------------------------------------------- verses
def process_verse(body, hint):
    body = re.sub(r"\[\d+\]|\(\d+\)", " ", body)
    body = body.replace("،", " ").replace(",", " ")
    frags = [f.strip() for f in re.split(r"\s*(?:\*|۝|\.\.\.|…)\s*", body) if f.strip()]
    found, after = [], None
    for f in frags:
        r = Q.find(f, hint, after)
        if r is None:
            found = None
            break
        found.append(r)
        after = r[1]
    if not found:
        return None
    out, refs = [], []
    for i, (w1, w2, exact) in enumerate(found):
        if i:
            pw = found[i - 1][1]
            if w1 != pw + 1:
                out.append(" … ")
            else:
                out.append(" ")
        # words, with an end-of-verse sign where a verse ends inside the quotation
        for w in range(w1, w2 + 1):
            out.append(Q.words[w][2])
            s, a, _ = Q.words[w]
            if w < w2 or (i + 1 < len(found) and found[i + 1][0] == w2 + 1):
                ns, na, _ = Q.words[w + 1]
                if (ns, na) != (s, a):
                    out.append(" ۝" + str(a).translate(AR_DIGITS))
            if w < w2:
                out.append(" ")
        refs.append(Q.ref(w1, w2))
    # one reference for the whole passage
    s1, a1, _, _ = refs[0]
    _, _, s2, a2 = refs[-1]
    merged = [(s1, a1, s2, a2)] if s1 == s2 and a2 >= a1 and a2 - a1 < 15 else refs
    return "".join(out), quran_note(merged)


# ----------------------------------------------------------------------------- paragraphs
class Ctx:
    def __init__(self):
        self.notes = []        # footnote texts, in order (per chapter)
        self.verses = []       # verse html
        self.srclist = {}      # [n] -> source text (topic source list)
        self.paren_list = False


def tok_note(ctx, text):
    ctx.notes.append(clean_note(text))
    return "%d" % (len(ctx.notes) - 1)


def tok_verse(ctx, text):
    ctx.verses.append(text)
    return "%d" % (len(ctx.verses) - 1)


def honorifics(t):
    t = t.replace("صلى الله عليه وآله وسلم", "صلى الله عليه وآله")
    t = re.sub(r"\s*ﷺ", " (صلّى الله عليه وآله)", t)
    t = t.replace("(ص)", "(صلّى الله عليه وآله)")
    t = re.sub(r"((?:الأئمة|الأطهار|أهل البيت|بيت النّبوّة|بيت النبوة)\s*)\(ع\)", r"\1(عليهم السلام)", t)
    t = re.sub(r"((?:الزهراء|فاطمة|مريم|زينب)\s*)\(ع\)", r"\1(عليها السلام)", t)
    t = t.replace("(ع)", "(عليه السلام)")
    return t


def spelling(t):
    t = re.sub(r"(?<![ء-ي])الإ(?=(?:ست|قت|نت|بت|جت|فت|لت|عت|حت|رت|نف|نق|نك|نس|نش|نح|نط|نع|ند|نب))", "الا", t)
    t = re.sub(r"(?<![ء-ي])الانسان", "الإنسان", t)
    t = re.sub(r"(?<![ء-ي])الى(?![ء-ي])", "إلى", t)
    t = re.sub(r"إنشاء الله", "إن شاء الله", t)
    return t


def quotes(t):
    t = t.replace("“", "«").replace("”", "»").replace("’", "«").replace("‘", "»")
    t = re.sub(r'"([^"\n]+)"', r"«\1»", t)
    t = t.replace('"', "")
    t = re.sub(r"(?<![\w])'([^'\n]{2,80})'", r"«\1»", t)
    return t


def spacing(t):
    t = t.replace("...", "…")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\s+([،؛:.!؟?…»\)\]])", r"\1", t)
    t = re.sub(r"([«\(\[])\s+", r"\1", t)
    t = re.sub(r"([،؛:!؟])(?=[^!؟\s\d؀-ؠ»\)\]-…])", r"\1 ", t)
    t = re.sub(r"\.(?=[ء-ي])", ". ", t)
    t = re.sub(r"؛\s*؛", "؛", t)
    t = re.sub(r"\.{2,}", ".", t)
    return t.strip()


def convert(ctx, t):
    """manuscript paragraph -> text with n footnote and n verse tokens"""
    t = t.strip()
    t = re.sub(r"^>\s*", "", t)
    t = re.sub(r"^\.\s+", "", t)
    t = t.replace("**.**", ".").replace("****", "").replace("**،**", "،")
    t = re.sub(r"(?<!\w)_(?=\S)|(?<=\S)_(?!\w)", "", t)

    # existing Word footnotes first (they may follow verses)
    t = re.sub(r"⟦FN:\s*(.*?)⟧", lambda m: "" + m.group(1).replace("[", "⦗").replace("]", "⦘") + "", t)

    # verses ﴿…﴾ / {…} with an optional reference after them
    def verse(m):
        body = m.group(1)
        rest = t_rest = ""
        return body

    out, pos = [], 0
    for m in re.finditer(r"[﴿{]([^﴾}]+)[﴾}]", t):
        out.append(t[pos:m.start()])
        body = m.group(1)
        pos = m.end()
        hint, qm = None, None
        while True:                      # consume the references that follow the verse
            tail = t[pos:]
            mm = QREF.match(tail)
            if mm:
                hint, qm = parse_qref(mm) or hint, mm
                pos += mm.end()
                continue
            mm = re.match(r"\s*\.?\s*\ue004([^\ue005]*)\ue005", tail)
            if mm and re.search("سورة|القرآن", mm.group(1)):
                q = QREF.search("[" + mm.group(1).replace("القرآن الكريم", "").strip(" .:،") + "]")
                if q:
                    hint = parse_qref(q) or hint
                pos += mm.end()
                continue
            mm = re.match(r"\s*\[(\d+)\]", tail)
            if mm and "سورة" in ctx.srclist.get(int(mm.group(1)), ""):
                q = QREF.search("[" + ctx.srclist[int(mm.group(1))].replace("القرآن الكريم", "").strip(" .:،") + "]")
                if q:
                    hint = parse_qref(q) or hint
                pos += mm.end()
                continue
            mm = re.match(r"\s*\((\d)\)", tail)
            if mm and ctx.paren_list and "سورة" in ctx.srclist.get(int(mm.group(1)), ""):
                pos += mm.end()
                continue
            break
        mm = qm
        res = process_verse(body, hint)
        if res:
            vtext, note = res
            out.append(tok_verse(ctx, "﴿" + vtext + "﴾") + tok_note(ctx, note))
        else:
            report.append("verse not found: " + body[:60])
            v = tok_verse(ctx, "﴿" + body.strip() + "﴾")
            if hint and mm and mm.re is QREF:
                a, b = mm.group("a").translate(WEST), (mm.group("b") or "").translate(WEST)
                v += tok_note(ctx, quran_note([(hint, int(a), hint, int(b or a))]))
            out.append(v)
    out.append(t[pos:])
    t = "".join(out)

    # Word footnotes -> notes
    t = re.sub(r"\s*([^]*)", lambda m: tok_note(ctx, m.group(1).replace("⦗", "[").replace("⦘", "]")), t)

    # numbered references to the topic's source list
    if ctx.srclist:
        def ref(m):
            n = int(m.group(1))
            if n in ctx.srclist:
                return tok_note(ctx, ctx.srclist[n])
            report.append("unknown ref [%d]" % n)
            return ""
        t = re.sub(r"\s*\[(\d+)\]", ref, t)
        if ctx.paren_list:
            t = re.sub(r"\s*\((\d)\)", ref, t)

    # inline sources: [ … ] containing a book name, anywhere
    t = re.sub(r"\s*\[\s*([^\[\]]*?(?:%s)[^\[\]]*?)\s*\]" % KW, lambda m: tok_note(ctx, m.group(1)), t)
    # ( … ) containing a book name, right after a quotation or at the end of a sentence
    t = re.sub(r"([»\"”]\**)(\s*[.،؛]?\s*)\(\s*((?:[^()]|\([^()]*\))*?(?:%s)(?:[^()]|\([^()]*\))*?)\s*\)" % KW,
               lambda m: m.group(1) + tok_note(ctx, m.group(3)) + m.group(2).strip(), t)
    t = re.sub(r"\s*\(\s*((?:المصدر)\s*:(?:[^()]|\([^()]*\))*?)\s*\)", lambda m: tok_note(ctx, m.group(1)), t)
    # quran refs left without a verse sign: [النساء: 10] after a quotation in «»
    t = QREF.sub(lambda m: tok_note(ctx, "سورة %s، الآية %s" % (Q.names.get(parse_qref(m), m.group("name")),
                                                            m.group("a") + ("–" + m.group("b") if m.group("b") else "")))
                 if parse_qref(m) else m.group(0), t)

    t = honorifics(t)
    t = spelling(t)
    t = quotes(t)
    t = spacing(t)
    t = re.sub("\\.((?:\\d+)+)\\s*\\.", "\\1.", t)
    # a note token directly after a full stop belongs before it
    t = re.sub(r"\.((?:\d+)+)", r"\1.", t)
    return t


TASHKEEL = re.compile("[\u064B-\u0652\u0670\u0640]")
VOWELS = re.compile("[\u064E-\u0650\u0652\u0670\u0640]")      # fatha, damma, kasra, sukun, dagger alif, tatweel


SHADDA_WORDS = [
    (r"السلام(?![\u0621-\u064A])", "السّلام"),
    (r"اللهم(?![\u0621-\u064A])", "اللهمّ"),
    (r"(?<![\u0621-\u064A])(و?ف?)صلى(?![\u0621-\u064A])", r"\1صلّى"),
    (r"(?<![\u0621-\u064A\u0651])كيفية(?![\u0621-\u064A])", "كيفيّة"),
    (r"(?<![\u0621-\u064A\u0651])السجادية(?![\u0621-\u064A])", "السجّاديّة"),
]


def shadda_words(t):
    """words that must always carry their shadda (the formulas after the Imams' names, اللهمّ …)"""
    for pat, rep in SHADDA_WORDS:
        t = re.sub(pat, rep, t)
    return t


def plain_ar(t):
    """one style for the whole book outside the Qur'an: shadda and tanween only"""
    t = VOWELS.sub("", t)
    t = shadda_words(t)
    t = re.sub("\u064B(\u0651?)\u0627", "\\1\u0627\u064B", t)       # fathatan on the alif: كتاباً
    t = re.sub("(?<![\u0621-\u064A])([وفبكتل]?)(ال|ل)\u0644\u0651(?=\u0647)", "\\1\\2\u0644", t)   # الله, لله, بالله: no shadda
    return t


def render_inline(ctx, t):
    """tokens -> html"""
    t = plain_ar(t)
    t = t.translate(AR_DIGITS)
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = t.replace("**", "")
    # hadith / sayings in «»
    t = re.sub(r"«([^«»]{12,})»", r'<span class="q">«\1»</span>', t)
    t = re.sub(r"(\d+)", lambda m: '<span class="ayah">%s</span>' % html.escape(ctx.verses[int(m.group(1))]), t)
    t = re.sub(r"(\d+)",
               lambda m: '<span class="fn" data-note="%s"></span>' % html.escape(shadda_words(ctx.notes[int(m.group(1))]).translate(AR_DIGITS), quote=True), t)
    return t


# ----------------------------------------------------------------------------- structure
def plain(s):
    return re.sub(r"\*\*|^>\s*", "", s).strip()


def is_heading(p):
    s = re.sub(r"^>\s*", "", p.strip())
    return s.startswith("**") and s.endswith("**") and len(plain(s)) < 70 and "**" not in s[2:-2]


def K(s):
    """structural key: the text without any vowel marks or shadda (the headings are vowelled in the final text)"""
    return re.sub("[\u064B-\u0652\u0670\u0640]", "", s)


SUBHEADS_K = tuple(K(x) for x in SUBHEADS)


def parse():
    paras = [l for l in open(TEXT, encoding="utf8").read().split("\n") if l.strip()]
    i = [K(p) for p in paras].index("**المقدمة**")
    intro_end = [K(p) for p in paras].index("**الإهداء**")
    chapters = [{"title": "المقدمة", "paras": paras[i + 1:intro_end], "kind": "intro"}]
    cur = {"title": "الإهداء", "paras": [], "kind": "dedication"}
    chapters.append(cur)
    for p in paras[intro_end + 1:]:
        s = plain(p)
        if is_heading(p) and not K(s).startswith(SUBHEADS_K) and not re.match(r"^\[\d+\]", s):
            cur = {"title": s, "paras": [], "kind": "topic"}
            chapters.append(cur)
        elif cur["kind"] == "dedication" and K(s) == "اللطف الإلهي":
            cur = {"title": s, "paras": [], "kind": "topic"}
            chapters.append(cur)
        else:
            cur["paras"].append(p)
    # «اللطف الإلهي» is a plain-text title inside the first topic
    out = []
    for ch in chapters:
        keys = [K(p) for p in ch["paras"]]
        if ch["kind"] == "topic" and "اللطف الإلهي" in keys:
            k = keys.index("اللطف الإلهي")
            out.append({"title": ch["title"], "paras": ch["paras"][:k], "kind": "topic"})
            out.append({"title": ch["paras"][k], "paras": ch["paras"][k + 1:], "kind": "topic"})
        else:
            out.append(ch)
    return out


def take_sources(ch, ctx):
    """remove the topic's source list from its paragraphs and keep it in ctx.srclist"""
    keep = []
    bullets = []
    for p in ch["paras"]:
        s = plain(p).strip("* ")
        m = re.match(r"^\[(\d+)\]\s*(.*)$", s)
        if m and (len(s) < 400) and not re.search(r"«", s[:20]):
            item = m.group(2).strip()
            src = re.search(r"\(\s*المصدر\s*:\s*((?:[^()]|\([^()]*\))*)\)", item)
            ctx.srclist[int(m.group(1))] = src.group(1) if src else item
            continue
        if K(s) in ("الأحاديث والآثار:", "الهوامش والمصادر:"):
            continue
        if K(ch["title"]).startswith("سكرات الموت") and s.startswith("•"):
            bullets.append(s)
            continue
        keep.append(p)
    if bullets:
        ctx.paren_list = True
        for k, b in enumerate(bullets, 1):
            b = re.sub(r"\*\*[^*]*\*\*|^•\s*|^\.\s*", "", b).strip(" .")
            b = b.replace("الآيات 27-", "الآيتان 27–28")
            ctx.srclist[k] = b
    if K(ch["title"]) == "أبكي لظلمة قبري":
        ctx.srclist.update(GRAVE_SOURCES)
    ch["paras"] = keep


ORN = '<div class="orn"></div>'


def chapter_html(ch, num, topic_no):
    ctx = Ctx()
    take_sources(ch, ctx)
    body = []
    in_list = False
    for p in ch["paras"]:
        s = plain(p)
        if ch["kind"] == "dedication":
            body.append('<p class="ded">%s</p>' % render_inline(ctx, convert(ctx, p)))
            continue
        if is_heading(p) or K(s).startswith(SUBHEADS_K) and len(s) < 60:
            if in_list:
                pass
                in_list = False
            body.append('<h3>%s</h3>' % html.escape(plain_ar(s.strip(" :.")).translate(AR_DIGITS)))
            continue
        bullet = s.startswith("•")
        if bullet:
            p = re.sub(r"^>?\s*•\s*", "", p)
            if not in_list:
                pass
                in_list = True
        elif in_list:
            pass
            in_list = False
        if re.fullmatch(r"[\(\[]\s*(?:المصدر\s*:)?(?:[^\[\]]*?)(?:%s)[^\[\]]*[\)\]]\.?" % KW, s) and body:
            note = tok_note(ctx, s.strip("()[]. "))
            prev = body.pop()
            body.append(re.sub(r"(\.?)</p>$", lambda m: render_inline(ctx, note) + m.group(1) + "</p>", prev, count=1))
            continue
        t = convert(ctx, p)
        if not t:
            continue
        cls = ""
        if re.fullmatch(r"\d+(\d+)?[.،]?", t):
            cls = ' class="verse-block"'
        elif t.startswith("«") and t.rstrip(".").endswith(("»", "")) and len(t) < 900:
            cls = ' class="quote-block"'
        body.append(('<div class="li">%s</div>' if bullet else "<p%s>%%s</p>" % cls) % render_inline(ctx, t))
    # every topic ends with the closing doxology
    if ch["kind"] == "topic":
        tail = re.sub(r"<[^>]*>", "", "".join(body[-2:]))
        tail = TASHKEEL.sub("", tail).replace("\u0651", "")
        if not re.search(r"الحمد\s+لله\s+رب\s+العالمين\s*[.!]?\s*$", tail.strip()):
            body.append('<p class="hamd-end">والحمد لله ربّ العالمين.</p>')
    title = html.escape(plain_ar(ch["title"]).replace("...", "…"))
    cid = "ch%d" % num
    label = ""
    if ch["kind"] == "topic":
        label = ""
    cls = {"intro": "chapter intro", "dedication": "chapter dedication", "topic": "chapter"}[ch["kind"]]
    return ('<section class="%s" id="%s" data-title="%s"><div class="opener">%s<h2 class="ch-title">%s</h2>%s</div>\n%s\n</section>'
            % (cls, cid, title, label, title, ORN, "\n".join(body)))


# ----------------------------------------------------------------------------- sources page
# every book cited in the footnotes, with its author (القرآن الكريم first, the rest alphabetically)
BIBLIOGRAPHY = [
    ("الاثنا عشرية في المواعظ العددية", "محمد بن الحسن الحرّ العاملي"),
    ("الإرشاد في معرفة حجج الله على العباد", "الشيخ المفيد، محمد بن محمد بن النعمان"),
    ("إقبال الأعمال", "السيد علي بن موسى بن طاووس"),
    ("الأمالي", "الشيخ الصدوق، محمد بن علي بن بابويه القمّي"),
    ("الأمالي", "الشيخ الطوسي، محمد بن الحسن"),
    ("بحار الأنوار الجامعة لدرر أخبار الأئمّة الأطهار", "العلّامة محمد باقر المجلسي"),
    ("البرهان في تفسير القرآن", "السيد هاشم البحراني"),
    ("بصائر الدرجات", "محمد بن الحسن الصفّار"),
    ("تحف العقول عن آل الرسول", "ابن شعبة الحرّاني"),
    ("تصحيح اعتقادات الإمامية", "الشيخ المفيد"),
    ("التفسير المنسوب إلى الإمام الحسن العسكري (عليه السلام)", ""),
    ("تفسير العيّاشي", "محمد بن مسعود العيّاشي"),
    ("تفسير القمّي", "علي بن إبراهيم القمّي"),
    ("تفسير نور الثقلين", "الشيخ عبد علي العروسي الحويزي"),
    ("التوحيد", "الشيخ الصدوق"),
    ("تهذيب الأحكام", "الشيخ الطوسي"),
    ("ثواب الأعمال وعقاب الأعمال", "الشيخ الصدوق"),
    ("جامع الأخبار", "محمد بن محمد الشعيري"),
    ("جامع السعادات", "الشيخ محمد مهدي النراقي"),
    ("الخصال", "الشيخ الصدوق"),
    ("روضة الواعظين", "محمد بن الفتّال النيسابوري"),
    ("شرح نهج البلاغة", "ابن أبي الحديد المعتزلي"),
    ("الصحيفة السجّادية", "الإمام علي بن الحسين زين العابدين (عليه السلام)"),
    ("علل الشرائع", "الشيخ الصدوق"),
    ("عوالي اللآلي العزيزية في الأحاديث الدينية", "ابن أبي جمهور الأحسائي"),
    ("عيون أخبار الرضا (عليه السلام)", "الشيخ الصدوق"),
    ("عيون الحكم والمواعظ", "علي بن محمد الليثي الواسطي"),
    ("غرر الحكم ودرر الكلم", "عبد الواحد بن محمد التميمي الآمدي"),
    ("الكافي", "ثقة الإسلام محمد بن يعقوب الكليني"),
    ("كشف الغمّة في معرفة الأئمّة", "علي بن عيسى الإربلي"),
    ("كمال الدين وتمام النعمة", "الشيخ الصدوق"),
    ("الكنى والألقاب", "الشيخ عبّاس القمّي"),
    ("مجمع البيان في تفسير القرآن", "الشيخ الفضل بن الحسن الطبرسي"),
    ("المحاسن", "أحمد بن محمد بن خالد البرقي"),
    ("مختصر بصائر الدرجات", "الحسن بن سليمان الحلّي"),
    ("مستدرك الوسائل ومستنبط المسائل", "الميرزا حسين النوري الطبرسي"),
    ("مشكاة الأنوار في غرر الأخبار", "علي بن الحسن الطبرسي"),
    ("مصباح الشريعة", "المنسوب إلى الإمام جعفر الصادق (عليه السلام)"),
    ("مصباح المتهجّد", "الشيخ الطوسي"),
    ("معاني الأخبار", "الشيخ الصدوق"),
    ("مكارم الأخلاق", "الحسن بن الفضل الطبرسي"),
    ("من لا يحضره الفقيه", "الشيخ الصدوق"),
    ("مناقب آل أبي طالب", "ابن شهرآشوب المازندراني"),
    ("ميزان الحكمة", "محمد الريشهري"),
    ("نهج البلاغة", "جمع الشريف الرضي"),
    ("وسائل الشيعة إلى تحصيل مسائل الشريعة", "محمد بن الحسن الحرّ العاملي"),
]


def bib_key(entry):
    t = re.sub(r"^ال", "", TASHKEEL.sub("", entry[0]))
    return t.translate(str.maketrans("أإآ", "ااا")), entry[1]


def bibliography_html():
    rows = ['<p class="bib"><span class="bt">القرآن الكريم.</span></p>']
    for title, author in sorted(BIBLIOGRAPHY, key=bib_key):
        title, author = TASHKEEL.sub("", title), TASHKEEL.sub("", author)      # plain, like the footnotes
        rows.append('<p class="bib"><span class="bt">%s</span>%s.</p>' % (
            html.escape(title), ("، " + html.escape(author)) if author else ""))
    return ('<section class="chapter biblio" id="biblio" data-title="المصادر والمراجع"><div class="opener">'
            '<h2 class="ch-title">المصادر والمراجع</h2>%s</div>\n%s\n</section>' % (ORN, "\n".join(rows)))


def front_matter():
    return """
<section class="title-page">
  <div class="tp-frame">
    <div class="tp-orn">۞</div>
    <h1 class="tp-title">%s</h1>
    <div class="tp-line"></div>
    <div class="tp-author-label">تأليف</div>
    <div class="tp-author">%s</div>
  </div>
</section>
<section class="basmala-page">
  <div class="basmala">بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ</div>
  <div class="hamd">
    <p>الحمد لله ربّ العالمين</p>
    <p>والصّلاة والسّلام على المبعوث رحمةً للعالمين</p>
    <p>محمّدٍ وآله الطّيّبين الطّاهرين</p>
  </div>
</section>
""" % (TITLE, AUTHOR)


def toc_html(chapters):
    rows = []
    for k, ch in enumerate(chapters):
        rows.append('<li><a href="#ch%d"><span class="t">%s</span><span class="fill"></span></a></li>' % (k, html.escape(ch["title"])))
    return ""


def main():
    chapters = parse()
    parts = [front_matter()]
    n = 0
    for k, ch in enumerate(chapters):
        n += ch["kind"] == "topic"
        parts.append(chapter_html(ch, k, n))
    parts.append(bibliography_html())
    parts.append(toc_html(chapters))
    tpl = open(P("book.css"), encoding="utf8").read()
    tpl += ".orn { background: url(%s) center / 62mm auto no-repeat; }\n" % O.data_uri(O.divider())
    tpl += ".tp-orn { background: url(%s) center / contain no-repeat; height: 15mm; color: transparent; }\n" % O.data_uri(
        O.svg(80, 80, O.khatam(40, 40, 34, O.GOLD, "#fff", 1.6)))
    tpl += ".tp-line { border: 0; height: 8mm; width: 62mm; background: url(%s) center / contain no-repeat; }\n" % O.data_uri(O.divider())
    tpl += ".ch-num { background: url(%s) center / 118mm auto no-repeat; }\n" % O.data_uri(O.headpiece())
    tpl += ".tp-frame { background: url(%s) top right / 17mm no-repeat, url(%s) top left / 17mm no-repeat, url(%s) bottom right / 17mm no-repeat, url(%s) bottom left / 17mm no-repeat; }\n" % tuple(
        O.data_uri(O.corner(fx=fx, fy=fy)) for fx, fy in ((True, False), (False, False), (True, True), (False, True)))
    doc = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>%s</title>
<style>%s</style>
<script src="../paginate.js"></script>
</head><body>
<div id="src">
%s
</div>
<div id="book"></div>
</body></html>""" % (TITLE, tpl, "\n".join(parts))
    open(P("build", "book.html"), "w", encoding="utf8").write(doc)
    open(P("build", "report.txt"), "w", encoding="utf8").write("\n".join(report))
    print("topics:", len(chapters), "report lines:", len(report))


if __name__ == "__main__":
    main()
