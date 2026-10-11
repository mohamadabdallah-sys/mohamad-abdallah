// Lesson deck: القوى وقوى العشرة (grade 7, section نور).
// usage: NODE_PATH=<dir with pptxgenjs, react, react-dom, react-icons, sharp> node make_ppt.js [applyTheme.js]
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react"), RDS = require("react-dom/server"), sharp = require("sharp");
const fa = require("react-icons/fa");

const OUT = path.join(__dirname, "عرض-القوى-وقوى-العشرة.pptx");
const THEME = {
  name: "Powers G7", headFontFace: "Arial", bodyFontFace: "Arial",
  colors: {
    dk1: "172231", lt1: "FFFFFF", dk2: "0F2350", lt2: "EEF2F8",
    accent1: "1B3A7A", accent2: "E9B44C", accent3: "0E7C7B", accent4: "C2452F", accent5: "2F7D46", accent6: "7A3E8E",
    hlink: "2B5FB3", folHlink: "7A3E8E",
  },
};
const MATH = "Cambria";

async function icon(name, color = "#FFFFFF", px = 256) {
  const svg = RDS.renderToStaticMarkup(React.createElement(fa[name], { color, size: px }));
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// "2^{5} × 3^2" -> text runs with superscripts
function runs(str, base = {}) {
  const out = [];
  let i = 0, buf = "";
  const push = (t, sup) => { if (t) out.push({ text: t, options: { ...base, ...(sup ? { superscript: true } : {}) } }); };
  while (i < str.length) {
    if (str[i] === "^") {
      push(buf); buf = "";
      if (str[i + 1] === "{") { const j = str.indexOf("}", i); push(str.slice(i + 2, j), true); i = j + 1; }
      else { push(str[i + 1], true); i += 2; }
    } else { buf += str[i]; i++; }
  }
  push(buf);
  return out;
}
// several lines -> runs with breakLine between lines
function lines(arr, base = {}, rtl = false) {
  const out = [];
  arr.forEach((l, k) => {
    const r = typeof l === "string" ? runs(l, base) : runs(l.t, { ...base, ...l.o });
    if (k < arr.length - 1) r[r.length - 1].options.breakLine = true;
    out.push(...r);
  });
  return out;
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.rtlMode = true;
  pres.title = "القوى وقوى العشرة";
  pres.subject = "رياضيات – الصف السابع";
  pres.author = "Mohamad Abdallah";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const shadow = () => ({ type: "outer", color: "1B2A44", opacity: 0.14, blur: 8, offset: 2, angle: 90 });

  const ICON = {};
  for (const n of ["FaBullseye", "FaBookOpen", "FaLayerGroup", "FaPuzzlePiece", "FaQuestion", "FaLightbulb", "FaUsers",
    "FaCalculator", "FaRulerHorizontal", "FaFileAlt", "FaIdCard", "FaMoon", "FaExclamationTriangle", "FaHome",
    "FaCube", "FaListOl", "FaHandsHelping", "FaRocket", "FaCheck", "FaTimes", "FaHeart", "FaBrain", "FaHandPaper", "FaFlagCheckered"])
    ICON[n] = await icon(n);

  // ---------- layouts ----------
  pres.defineSlideMaster({
    title: "DARK", background: { color: C.text2 },
    objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.73, h: 1.4, fontSize: 48, bold: true,
      color: C.background1, align: "right", valign: "middle", rtlMode: true }, text: "" } }],
  });
  pres.defineSlideMaster({
    title: "CONTENT", background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 4.2, y: 0.32, w: 8.53, h: 0.85, fontSize: 32, bold: true,
        color: C.text2, align: "right", valign: "middle", rtlMode: true, margin: 0 }, text: "" } },
      { text: { text: "القوى وقوى العشرة · الصف السابع – شعبة نور", options: { x: 6.73, y: 7.02, w: 6.0, h: 0.3, fontSize: 10,
        color: "7C8797", align: "right", rtlMode: true, margin: 0 } } },
    ],
    slideNumber: { x: 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: "7C8797", margin: 0 },
  });

  // ---------- helpers ----------
  const ar = (s, t, o) => s.addText(Array.isArray(t) ? t : runs(t, { rtlMode: true, lang: "ar-SA" }),
    { isTextBox: true, rtlMode: true, lang: "ar-SA", align: "right", valign: "top", fontSize: 16, color: C.text1, margin: 0.05, ...o });
  const mt = (s, t, o) => s.addText(Array.isArray(t) ? t : runs(t), { isTextBox: true, fontFace: MATH, align: "center",
    valign: "middle", fontSize: 26, color: C.text1, margin: 0.05, ...o });
  const card = (s, x, y, w, h, o = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: o.fill || C.background2, transparency: o.tr || 0 }, line: { color: o.line || o.fill || C.background2, width: o.lw || 0.75, transparency: o.ltr ?? (o.tr || 0) },
    shadow: o.noShadow ? undefined : shadow(), objectName: o.name });
  const badge = (s, x, y, d, ic, color) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color } });
    if (ic) s.addImage({ data: ICON[ic], x: x + d * 0.26, y: y + d * 0.26, w: d * 0.48, h: d * 0.48 });
  };
  const num = (s, x, y, d, n, color) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color } });
    s.addText(String(n), { isTextBox: true, x, y, w: d, h: d, fontSize: d * 26, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
  };
  const chip = (s, text, color, ic) => { // phase + time tag, top-left
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 0.47, w: 3.3, h: 0.55, rectRadius: 0.27, fill: { color }, line: { color } });
    if (ic) s.addImage({ data: ICON[ic], x: 3.43, y: 0.59, w: 0.31, h: 0.31 });
    s.addText(text, { isTextBox: true, x: 0.75, y: 0.47, w: ic ? 2.6 : 3.0, h: 0.55, fontSize: 14, bold: true, color: C.background1,
      align: "center", valign: "middle", rtlMode: true, lang: "ar-SA", margin: 0 });
  };
  const content = (sec, title, notes) => {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: sec });
    s.addText(runs(title, { rtlMode: true }), { placeholder: "title", rtlMode: true, lang: "ar-SA" });
    if (notes) s.addNotes(notes);
    return s;
  };
  const arrowDown = (s, x, y, w, h, color) => s.addShape(pres.shapes.DOWN_ARROW, { x, y, w, h, fill: { color }, line: { color } });
  const arrowLeft = (s, x, y, w, h, color) => s.addShape(pres.shapes.LEFT_ARROW, { x, y, w, h, fill: { color }, line: { color } });

  // =====================================================================
  // 1. Title
  pres.addSection({ title: "البداية" });
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "البداية" });
    s.addText("القوى وقوى العشرة", { placeholder: "title", rtlMode: true, lang: "ar-SA" });
    ar(s, "رياضيات · الصف السابع – شعبة نور · مدّة الحصّة 50 دقيقة", { x: 5.0, y: 3.35, w: 7.53, h: 0.5, fontSize: 20, color: C.background2 });
    // big power on the left
    card(s, 0.8, 1.55, 4.6, 2.6, { fill: C.accent1, noShadow: true });
    mt(s, runs("2^{10}", { color: C.accent2, fontSize: 80, bold: true }), { x: 0.8, y: 1.6, w: 4.6, h: 1.6 });
    mt(s, "= 1024", { x: 0.8, y: 3.05, w: 4.6, h: 0.8, fontSize: 34, color: C.background1 });
    // values
    ar(s, "القيم", { x: 9.73, y: 4.75, w: 2.8, h: 0.45, fontSize: 18, bold: true, color: C.accent2 });
    const vals = [["الدقّة الرياضيّة", "FaCheck"], ["التفكير المنطقي", "FaBrain"], ["التعاون والعمل الجماعي", "FaHandsHelping"]];
    vals.forEach(([v, ic], k) => {
      const x = 12.53 - (k + 1) * 3.9 + 0.1 * k + 0.1;
      card(s, x, 5.3, 3.7, 0.8, { fill: C.accent1, noShadow: true });
      s.addImage({ data: ICON[ic], x: x + 3.1, y: 5.5, w: 0.4, h: 0.4 });
      ar(s, v, { x: x + 0.1, y: 5.3, w: 2.9, h: 0.8, fontSize: 17, bold: true, color: C.background1, valign: "middle" });
    });
    s.addNotes("ترحيب سريع بالتلاميذ، وتقسيمهم مسبقًا إلى مجموعات من 3 طلاب. نعرض عنوان الدرس ونترك العدد 1024 على الشاشة كسؤال مفتوح: كيف نحصل على 1024 من العدد 2؟");
  }

  // 2. Goals
  {
    const s = content("البداية", "أهداف الحصّة",
      "نقرأ الأهداف بسرعة مع التلاميذ. في نهاية الحصّة نعود إليها للتحقّق من تحقيقها. أنماط التعلّم المعتمدة: الرياضي-المنطقي (الاستنتاج والقواعد) والحركي-الجسدي (طيّ الورقة).");
    const goals = [
      "يكتب جداء عوامل متساوية على شكل قوّة a^n، ويحدّد الأساس والأُس.",
      "يحسب قيمة قوّة، ويحدّد إشارتها عندما يكون الأساس سالبًا.",
      "يستنتج قواعد الجداء والقسمة وقوّة القوّة لقوى لها الأساس نفسه، ويطبّقها.",
      "يفسّر لماذا a^0 = 1، ويكتب قوى العشرة.",
      "يطبّق أولويّات الحساب في عبارات تتضمّن قوى، ويتجنّب الأخطاء الشائعة.",
    ];
    ar(s, "في نهاية الحصّة يتوقّع أن يصبح التلميذ قادرًا على أن:", { x: 4.6, y: 1.35, w: 8.13, h: 0.45, fontSize: 16, color: "4F5C6E" });
    goals.forEach((g, k) => {
      const y = 1.9 + k * 0.97;
      card(s, 4.6, y, 8.13, 0.82, { fill: C.background2, noShadow: true });
      num(s, 12.0, y + 0.16, 0.5, k + 1, C.accent1);
      ar(s, g, { x: 4.75, y, w: 7.1, h: 0.82, fontSize: 16, valign: "middle" });
    });
    // side panel: learning styles
    card(s, 0.6, 1.35, 3.6, 5.37, { fill: C.text2, noShadow: true });
    ar(s, "أنماط التعلّم", { x: 0.8, y: 1.55, w: 3.2, h: 0.5, fontSize: 20, bold: true, color: C.accent2, align: "center" });
    [["رياضي – منطقي", "FaBrain", "نستنتج القواعد من الملاحظة"], ["حركي – جسدي", "FaHandPaper", "نطوي الورقة ونعدّ الطبقات"]].forEach(([t, ic, d], k) => {
      const y = 2.35 + k * 2.1;
      badge(s, 1.85, y, 1.1, ic, C.accent3);
      ar(s, t, { x: 0.8, y: y + 1.15, w: 3.2, h: 0.45, fontSize: 17, bold: true, color: C.background1, align: "center" });
      ar(s, d, { x: 0.8, y: y + 1.55, w: 3.2, h: 0.4, fontSize: 14, color: C.background2, align: "center" });
    });
  }

  // 3. Vocabulary
  {
    const s = content("البداية", "المصطلحات الجديدة",
      "نقدّم المصطلحات الستّة بالعربيّة والإنكليزيّة. نشير على الرسم: الرقم الكبير في الأسفل هو الأساس، والرقم الصغير المرتفع هو الأُس.");
    // diagram a^n
    card(s, 0.6, 1.4, 5.2, 5.3, { fill: C.background2, noShadow: true });
    mt(s, runs("a^n", { fontSize: 120, bold: true, color: C.text2, italic: true }), { x: 1.6, y: 2.6, w: 3.2, h: 2.4 });
    s.addShape(pres.shapes.LINE, { x: 3.65, y: 2.15, w: 0.65, h: 0.75, line: { color: C.accent4, width: 2.5, endArrowType: "triangle" } });
    ar(s, [{ text: "الأُس ", options: { bold: true, color: C.accent4, rtlMode: true } }, { text: "Exponent", options: { color: C.accent4 } }],
      { x: 2.4, y: 1.6, w: 3.2, h: 0.5, fontSize: 18, align: "center" });
    s.addShape(pres.shapes.LINE, { x: 2.45, y: 4.75, w: 0.35, h: 0.75, flipV: true, line: { color: C.accent3, width: 2.5, endArrowType: "triangle" } });
    ar(s, [{ text: "الأساس ", options: { bold: true, color: C.accent3, rtlMode: true } }, { text: "Base", options: { color: C.accent3 } }],
      { x: 0.9, y: 5.55, w: 3.4, h: 0.5, fontSize: 18, align: "center" });
    ar(s, "تُقرأ: a أُس n  ·  أو: a قوّة n", { x: 0.8, y: 6.1, w: 4.8, h: 0.45, fontSize: 14, color: "4F5C6E", align: "center" });
    // term grid 2 x 3
    const terms = [
      ["القوّة", "Power", "2^5"], ["الأساس", "Base", "2^5 ← 2"], ["الأُس", "Exponent", "2^5 ← 5"],
      ["المربّع", "Square", "a^2 = a × a"], ["المكعّب", "Cube", "a^3 = a × a × a"], ["قوى العشرة", "Powers of ten", "10^n"],
    ];
    const colors = [C.accent1, C.accent3, C.accent4, C.accent5, C.accent6, C.accent2];
    terms.forEach(([a, e, m], k) => {
      const col = k % 2, row = Math.floor(k / 2);
      const x = 12.73 - (col + 1) * 3.35 - col * 0.25, y = 1.4 + row * 1.85;
      card(s, x, y, 3.35, 1.6, { fill: C.background1, line: "DCE2E9" });
      s.addShape(pres.shapes.OVAL, { x: x + 2.85, y: y + 0.2, w: 0.3, h: 0.3, fill: { color: colors[k] }, line: { color: colors[k] } });
      ar(s, a, { x: x + 0.15, y: y + 0.1, w: 2.65, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
      ar(s, e, { x: x + 0.15, y: y + 0.6, w: 3.05, h: 0.38, fontSize: 14, color: "4F5C6E", rtlMode: false });
      mt(s, m.replace(" ← ", "  →  "), { x: x + 0.15, y: y + 0.98, w: 3.05, h: 0.5, fontSize: 18, color: colors[k], align: "left" });
    });
  }

  // 4. Warm-up question
  pres.addSection({ title: "التمهيد" });
  {
    const s = content("التمهيد", "كيف نكتبه بطريقة مختصرة؟",
      "التمهيد (5 د) – ربط بالمكتسبات السابقة: الضرب المتكرّر. نطرح السؤال ونسمع إجابات التلاميذ دون تصحيح. كثيرون سيقولون 2 × 5 = 10. نسأل: هل 2 × 5 تعني ضرب 2 في نفسه خمس مرّات؟");
    chip(s, "التمهيد · 5 د", C.accent3, "FaLightbulb");
    for (let k = 0; k < 5; k++) {
      const x = 1.55 + k * 2.2;
      s.addShape(pres.shapes.OVAL, { x, y: 1.75, w: 1.5, h: 1.5, fill: { color: C.accent2 }, line: { color: C.accent2 }, shadow: shadow() });
      mt(s, "2", { x, y: 1.75, w: 1.5, h: 1.5, fontSize: 54, bold: true, color: C.text2 });
      if (k < 4) mt(s, "×", { x: x + 1.5, y: 1.75, w: 0.7, h: 1.5, fontSize: 40, color: C.text2 });
    }
    card(s, 1.6, 3.85, 10.13, 1.15, { fill: C.background2, noShadow: true });
    mt(s, "2 × 2 × 2 × 2 × 2 = ?", { x: 1.6, y: 3.85, w: 10.13, h: 1.15, fontSize: 40, bold: true, color: C.text2 });
    card(s, 3.67, 5.45, 6.0, 1.0, { fill: C.accent4, tr: 88, line: C.accent4, ltr: 40, noShadow: true });
    ar(s, [{ text: "وهل يساوي ", options: { rtlMode: true } }, { text: "2 × 5", options: { fontFace: MATH, bold: true } }, { text: " ؟", options: {} }],
      { x: 3.67, y: 5.45, w: 6.0, h: 1.0, fontSize: 28, align: "center", valign: "middle", color: C.accent4 });
  }

  // 5. Warm-up answer
  {
    const s = content("التمهيد", "القوّة: ضرب عدد في نفسه عدّة مرّات",
      "نقدّم القوّة كطريقة مختصرة لكتابة ضرب عدد في نفسه عدّة مرّات: 2 × 2 × 2 × 2 × 2 = 2^5 = 32. ونقارن مع 2 × 5 = 10 الذي هو جمع 2 خمس مرّات. ننتقل بعدها إلى نشاط الاستكشاف.");
    chip(s, "التمهيد · 5 د", C.accent3, "FaLightbulb");
    // right: correct
    card(s, 6.83, 1.5, 5.9, 4.4, { fill: C.accent5, tr: 90, line: C.accent5, ltr: 30 });
    badge(s, 11.7, 1.75, 0.75, "FaCheck", C.accent5);
    ar(s, "خمسة عوامل كلّها 2", { x: 7.0, y: 1.8, w: 4.5, h: 0.6, fontSize: 20, bold: true, color: C.accent5 });
    mt(s, "2 × 2 × 2 × 2 × 2", { x: 6.83, y: 2.65, w: 5.9, h: 0.8, fontSize: 30 });
    mt(s, runs("= 2^5 = 32", { bold: true }), { x: 6.83, y: 3.5, w: 5.9, h: 1.1, fontSize: 52, color: C.accent5 });
    ar(s, "نقرأ: 2 أُس 5", { x: 6.95, y: 4.9, w: 5.65, h: 0.5, fontSize: 18, align: "center", color: C.text1 });
    // left: wrong
    card(s, 0.6, 1.5, 5.9, 4.4, { fill: C.accent4, tr: 90, line: C.accent4, ltr: 30 });
    badge(s, 5.45, 1.75, 0.75, "FaTimes", C.accent4);
    ar(s, "هذا جمع 2 خمس مرّات", { x: 0.75, y: 1.8, w: 4.6, h: 0.6, fontSize: 20, bold: true, color: C.accent4 });
    mt(s, "2 + 2 + 2 + 2 + 2", { x: 0.6, y: 2.65, w: 5.9, h: 0.8, fontSize: 30 });
    mt(s, runs("= 2 × 5 = 10", { bold: true }), { x: 0.6, y: 3.5, w: 5.9, h: 1.1, fontSize: 52, color: C.accent4 });
    ar(s, "ليس هو الجداء المطلوب", { x: 0.75, y: 4.9, w: 5.6, h: 0.5, fontSize: 18, align: "center" });
    card(s, 2.17, 6.15, 9.0, 0.65, { fill: C.text2, noShadow: true });
    mt(s, [...runs("2^5 = 32  ≠  2 × 5 = 10", { color: C.accent2, bold: true })], { x: 2.17, y: 6.15, w: 9.0, h: 0.65, fontSize: 26 });
  }

  // 6. Group work setup
  pres.addSection({ title: "الاستكشاف" });
  {
    const s = content("الاستكشاف", "نعمل في مجموعات من 3 طلاب",
      "الاستكشاف (30 د) – الاستراتيجيّة: العمل الجماعي والتعلّم بالاكتشاف. نوزّع على كل مجموعة: ورقة A4، مسطرة، آلة حاسبة، وبطاقات الأنشطة. نقترح توزيع الأدوار: الطاوي يطوي الورقة، العادّ يعدّ الطبقات، المسجّل يكتب في الجدول، ويتبادلون الأدوار في كل نشاط.");
    chip(s, "الاستكشاف · 30 د", C.accent1, "FaUsers");
    ar(s, "الوسائل", { x: 6.83, y: 1.4, w: 5.9, h: 0.5, fontSize: 22, bold: true, color: C.text2 });
    const tools = [["ورقة A4", "FaFileAlt"], ["مسطرة", "FaRulerHorizontal"], ["آلة حاسبة", "FaCalculator"], ["بطاقة الشرح «القوى وقواعدها»", "FaIdCard"]];
    tools.forEach(([t, ic], k) => {
      const y = 2.05 + k * 1.1;
      card(s, 6.83, y, 5.9, 0.9, { fill: C.background2, noShadow: true });
      badge(s, 11.9, y + 0.12, 0.66, ic, C.accent1);
      ar(s, t, { x: 7.0, y, w: 4.8, h: 0.9, fontSize: 18, valign: "middle" });
    });
    ar(s, "أدوار المجموعة", { x: 0.6, y: 1.4, w: 5.8, h: 0.5, fontSize: 22, bold: true, color: C.text2 });
    const roles = [["الطاوي", "يطوي الورقة من المنتصف", C.accent3], ["العادّ", "يعدّ الطبقات بعد كل طيّة", C.accent6], ["المسجّل", "يدوّن النتائج في الجدول", C.accent4]];
    roles.forEach(([r, d, col], k) => {
      const y = 2.05 + k * 1.47;
      card(s, 0.6, y, 5.8, 1.27, { fill: col, tr: 88, line: col, ltr: 50, noShadow: true });
      num(s, 5.55, y + 0.29, 0.7, k + 1, col);
      ar(s, r, { x: 0.8, y: y + 0.13, w: 4.6, h: 0.5, fontSize: 20, bold: true, color: col });
      ar(s, d, { x: 0.8, y: y + 0.63, w: 4.6, h: 0.5, fontSize: 16 });
    });
    ar(s, "نتبادل الأدوار في كل نشاط", { x: 0.6, y: 6.45, w: 5.8, h: 0.4, fontSize: 14, color: "4F5C6E", align: "center" });
  }

  // 7. Activity 1 – folding (task)
  const foldTable = (s, x, y, w, layers, powers) => {
    const cols = ["0", "1", "2", "3", "4", "5", "10"];
    const head = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 }, rtlMode: true, align: "center" } });
    const cell = (t, o = {}) => ({ text: Array.isArray(t) ? t : runs(t), options: { align: "center", fontFace: MATH, ...o } });
    const rows = [
      [...cols.slice().reverse().map((c) => cell(c, { bold: true, fill: { color: C.background2 } })), head("عدد الطيّات")],
      [...layers.slice().reverse().map((c) => cell(c)), head("عدد الطبقات")],
      [...powers.slice().reverse().map((c) => cell(runs(c, { fontFace: MATH }), { color: C.accent3, bold: true })), head("على شكل قوّة للعدد 2")],
    ];
    const lab = 2.9, cw = (w - lab) / 7;
    s.addTable(rows, { x, y, w, colW: [...Array(7).fill(cw), lab], rowH: [0.62, 0.72, 0.72], fontSize: 20, valign: "middle",
      border: { type: "solid", pt: 1, color: "C9D2DE" }, color: C.text1 });
  };
  {
    const s = content("الاستكشاف", "النشاط 1 – طيّ الورقة",
      "يطوي كل فريق ورقة A4 من المنتصف مرّة بعد مرّة، ويعدّ الطبقات بعد كل طيّة ويسجّلها في الجدول. نلاحظ أن الطيّ يصبح صعبًا جدًّا بعد 6 أو 7 طيّات، لذلك نكمل الجدول للعمود 10 بالتفكير: كل طيّة تضاعف عدد الطبقات.");
    chip(s, "الاستكشاف · النشاط 1", C.accent1, "FaLayerGroup");
    const steps = ["اطوِ ورقة A4 من المنتصف.", "عُدّ الطبقات بعد كل طيّة وسجّلها في الجدول.", "اكتب عدد الطبقات على شكل قوّة للعدد 2."];
    steps.forEach((t, k) => {
      const x = 12.73 - (k + 1) * 3.95 - k * 0.12 + 0.12 * 0;
      card(s, x, 1.45, 3.95, 1.45, { fill: C.background2, noShadow: true });
      num(s, x + 3.3, 1.6, 0.5, k + 1, C.accent1);
      ar(s, t, { x: x + 0.15, y: 1.6, w: 3.05, h: 1.2, fontSize: 17 });
    });
    foldTable(s, 0.6, 3.4, 12.13, ["1", "?", "?", "?", "?", "?", "?"], ["2^0", "?", "?", "?", "?", "?", "?"]);
    card(s, 2.67, 5.85, 8.0, 0.85, { fill: C.accent2, tr: 80, line: C.accent2, ltr: 20, noShadow: true });
    ar(s, "ماذا يحدث لعدد الطبقات بعد كل طيّة؟", { x: 2.67, y: 5.85, w: 8.0, h: 0.85, fontSize: 22, bold: true, align: "center", valign: "middle", color: C.text2 });
  }

  // 8. Activity 1 – results
  {
    const s = content("الاستكشاف", "كل طيّة تضاعف عدد الطبقات",
      "نجمع نتائج المجموعات ونتحقّق: 1، 2، 4، 8، 16، 32 أي 2^0، 2^1، 2^2، … . الأُس يساوي عدد الطيّات. وبعد 10 طيّات: 2^10 = 1024 طبقة (نتحقّق بالآلة الحاسبة).");
    chip(s, "الاستكشاف · النشاط 1", C.accent1, "FaLayerGroup");
    foldTable(s, 0.6, 1.4, 12.13, ["1", "2", "4", "8", "16", "32", "1024"], ["2^0", "2^1", "2^2", "2^3", "2^4", "2^5", "2^{10}"]);
    s.addChart(pres.charts.BAR, [{ name: "عدد الطبقات", labels: ["0", "1", "2", "3", "4", "5"], values: [1, 2, 4, 8, 16, 32] }], {
      x: 0.6, y: 3.75, w: 7.2, h: 3.05, barDir: "col", chartColors: ["0E7C7B"], showValue: true, dataLabelPosition: "outEnd",
      dataLabelColor: "172231", dataLabelFontSize: 13, dataLabelFontFace: "+mn-lt", showLegend: false,
      showTitle: true, title: "عدد الطبقات حسب عدد الطيّات", titleFontSize: 14, titleColor: "4F5C6E", titleFontFace: "+mn-lt",
      catAxisLabelColor: "4F5C6E", valAxisLabelColor: "4F5C6E", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
      catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, valGridLine: { color: "E2E7EE", size: 0.75 }, catGridLine: { style: "none" },
      valAxisMaxVal: 36, valAxisMinVal: 0, valAxisMajorUnit: 8, barGapWidthPct: 60,
    });
    card(s, 8.2, 3.85, 4.53, 2.9, { fill: C.text2 });
    ar(s, "بعد 10 طيّات", { x: 8.35, y: 4.0, w: 4.23, h: 0.5, fontSize: 18, bold: true, color: C.accent2, align: "center" });
    mt(s, runs("2^{10} = 1024", { bold: true }), { x: 8.2, y: 4.55, w: 4.53, h: 1.1, fontSize: 44, color: C.background1 });
    ar(s, "طبقة! الأُس = عدد الطيّات", { x: 8.35, y: 5.75, w: 4.23, h: 0.5, fontSize: 17, color: C.background2, align: "center" });
  }

  // 9. Activity 2 – task
  const act2 = [
    ["2^3 × 2^2", "(2×2×2) × (2×2)", "2^5", "5 عوامل"],
    ["3^2 × 3^4", "(3×3) × (3×3×3×3)", "3^6", "6 عوامل"],
    ["2^5 ÷ 2^2", "(2×2×2×2×2) ÷ (2×2)", "2^3", "نختصر عاملين"],
    ["(5^2)^3", "(5×5)(5×5)(5×5)", "5^6", "3 مجموعات من عاملين"],
  ];
  const act2Slide = (solved) => {
    const s = content("الاستكشاف", solved ? "النشاط 2 – نعدّ العوامل" : "النشاط 2 – من المفكّك إلى القاعدة",
      solved ? "نصحّح مع المجموعات: نفكّك كل قوّة إلى عوامل، نعدّها، ثم نكتب النتيجة قوّة واحدة. في القسمة نختصر العوامل المشتركة. في قوّة القوّة لدينا 3 مجموعات في كل منها عاملان."
        : "تفكّك كل مجموعة كل قوّة إلى عوامل، وتعدّها، ثم تكتب النتيجة قوّة واحدة. المتعثّرون يعتمدون على الكتابة المفكّكة والآلة الحاسبة للتحقّق قبل استعمال أي قاعدة.");
    chip(s, "الاستكشاف · النشاط 2", C.accent1, "FaPuzzlePiece");
    ar(s, "فكّك كل قوّة إلى عوامل، عُدّها، ثم اكتب النتيجة قوّة واحدة.", { x: 0.6, y: 1.35, w: 12.13, h: 0.5, fontSize: 18, color: "4F5C6E" });
    act2.forEach(([q, exp, ans, note], k) => {
      const y = 2.0 + k * 1.18;
      card(s, 0.6, y, 12.13, 1.0, { fill: k % 2 ? C.background1 : C.background2, line: "DCE2E9", noShadow: true });
      mt(s, q, { x: 9.9, y, w: 2.7, h: 1.0, fontSize: 30, bold: true, color: C.text2 });
      mt(s, "=", { x: 9.4, y, w: 0.5, h: 1.0, fontSize: 28 });
      mt(s, solved ? exp : "…………………………", { x: 4.9, y, w: 4.5, h: 1.0, fontSize: solved ? 24 : 22, color: solved ? C.text1 : "9AA5B4" });
      mt(s, "=", { x: 4.4, y, w: 0.5, h: 1.0, fontSize: 28 });
      if (solved) {
        mt(s, runs(ans, { bold: true }), { x: 2.9, y, w: 1.5, h: 1.0, fontSize: 32, color: C.accent3 });
        card(s, 0.8, y + 0.2, 2.0, 0.6, { fill: C.accent3, tr: 85, line: C.accent3, ltr: 60, noShadow: true });
        ar(s, note, { x: 0.8, y: y + 0.2, w: 2.0, h: 0.6, fontSize: 14, bold: true, color: C.accent3, align: "center", valign: "middle" });
      } else {
        mt(s, runs(ans[0] + "^?", { bold: true }), { x: 2.9, y, w: 1.5, h: 1.0, fontSize: 32, color: C.accent3 });
        ar(s, "عدد العوامل: ……", { x: 0.8, y, w: 2.0, h: 1.0, fontSize: 15, color: "7C8797", valign: "middle", align: "center" });
      }
    });
    return s;
  };
  act2Slide(false);
  act2Slide(true);

  // 11. Rules derived
  {
    const s = content("الاستكشاف", "نستنتج القواعد",
      "ننتقل من الأمثلة إلى القاعدة العامّة. نؤكّد أن القواعد صحيحة فقط عندما يكون الأساس نفسه. نسأل التلاميذ: ماذا نفعل بالأُسَّين في كل حالة؟ نجمع، نطرح، نضرب.");
    chip(s, "الاستكشاف · النشاط 2", C.accent1, "FaPuzzlePiece");
    const R = [
      ["جداء قوّتين", "a^m × a^n = a^{m+n}", "نجمع الأُسَّين", "2^3 × 2^2 = 2^5", C.accent1],
      ["قسمة قوّتين", "a^m ÷ a^n = a^{m−n}", "نطرح الأُسَّين", "2^5 ÷ 2^2 = 2^3", C.accent3],
      ["قوّة القوّة", "(a^m)^n = a^{m×n}", "نضرب الأُسَّين", "(5^2)^3 = 5^6", C.accent6],
    ];
    R.forEach(([t, rule, how, ex, col], k) => {
      const x = 12.73 - (k + 1) * 3.85 - k * 0.29;
      card(s, x, 1.45, 3.85, 4.75, { fill: C.background1, line: "DCE2E9" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.45, w: 3.85, h: 0.85, rectRadius: 0.12, fill: { color: col }, line: { color: col } });
      ar(s, t, { x, y: 1.45, w: 3.85, h: 0.85, fontSize: 22, bold: true, color: C.background1, align: "center", valign: "middle" });
      mt(s, runs(rule, { italic: true, bold: true }), { x: x + 0.1, y: 2.55, w: 3.65, h: 1.1, fontSize: 28, color: col });
      ar(s, how, { x: x + 0.2, y: 3.75, w: 3.45, h: 0.55, fontSize: 20, bold: true, align: "center", color: C.text1 });
      s.addShape(pres.shapes.LINE, { x: x + 0.5, y: 4.5, w: 2.85, h: 0, line: { color: "DCE2E9", width: 1 } });
      ar(s, "مثال", { x: x + 0.2, y: 4.65, w: 3.45, h: 0.4, fontSize: 14, color: "7C8797", align: "center" });
      mt(s, ex, { x: x + 0.1, y: 5.1, w: 3.65, h: 0.8, fontSize: 24 });
    });
    card(s, 2.67, 6.35, 8.0, 0.5, { fill: C.accent2, tr: 75, line: C.accent2, ltr: 30, noShadow: true });
    ar(s, "شرط مهمّ: الأساس نفسه في كل قاعدة", { x: 2.67, y: 6.35, w: 8.0, h: 0.5, fontSize: 17, bold: true, align: "center", valign: "middle", color: C.text2 });
  }

  // 12–13. Activity 3 – zero exponent
  const zeroSlide = (solved) => {
    const s = content("الاستكشاف", solved ? "لماذا a^0 = 1 ؟" : "النشاط 3 – لغز الأُس صفر",
      solved ? "كلّما نقص الأُس بواحد نقسم على 3، فنصل إلى 3^0 = 1. نتحقّق بقاعدة القسمة: 3^2 ÷ 3^2 = 3^{2−2} = 3^0، ومن جهة أخرى 9 ÷ 9 = 1، إذن 3^0 = 1. وهذا صحيح لكل عدد a غير معدوم."
        : "يكمل التلاميذ الجدول بملاحظة النمط: كلّما نقص الأُس بواحد نقسم على 3. نترك المجموعات تتوقّع قيمة 3^0 قبل الكشف.");
    chip(s, "الاستكشاف · النشاط 3", C.accent1, "FaQuestion");
    const P = [["3^4", "81"], ["3^3", "27"], ["3^2", "9"], ["3^1", "3"], ["3^0", "1"]];
    P.forEach(([p, v], k) => {
      const x = 10.53 - k * 2.45, y = 1.4 + k * 0.45;
      const last = k === 4;
      card(s, x, y, 2.2, 1.65, { fill: last ? C.accent2 : C.background2, line: last ? C.accent2 : "DCE2E9" });
      mt(s, runs(p, { bold: true }), { x, y: y + 0.08, w: 2.2, h: 0.8, fontSize: 38, color: C.text2 });
      const show = solved || k < 2;
      mt(s, show ? "= " + v : "= ?", { x, y: y + 0.85, w: 2.2, h: 0.7, fontSize: 32, bold: true, color: show ? (last ? C.text2 : C.accent3) : C.accent4 });
      if (k < 4) {
        arrowLeft(s, x - 0.3, y + 0.55, 0.55, 0.4, C.accent4);
        mt(s, "÷ 3", { x: x - 0.55, y: y + 0.98, w: 1.0, h: 0.45, fontSize: 18, bold: true, color: C.accent4 });
      }
    });
    card(s, 0.6, 5.0, 12.13, 1.75, { fill: solved ? C.text2 : C.background2, noShadow: true });
    if (solved) {
      ar(s, "نتحقّق بقاعدة القسمة:", { x: 8.6, y: 5.15, w: 3.95, h: 0.5, fontSize: 18, bold: true, color: C.accent2 });
      mt(s, runs("3^2 ÷ 3^2 = 3^{2−2} = 3^0", { color: C.background1 }), { x: 5.2, y: 5.6, w: 6.0, h: 0.65, fontSize: 28 });
      ar(s, "ومن جهة أخرى", { x: 3.5, y: 5.6, w: 1.8, h: 0.65, fontSize: 16, color: C.background2, valign: "middle", align: "center" });
      mt(s, "9 ÷ 9 = 1", { x: 0.8, y: 5.6, w: 2.7, h: 0.65, fontSize: 28, color: C.background1 });
      mt(s, runs("a^0 = 1   (a ≠ 0)", { bold: true, color: C.accent2 }), { x: 0.8, y: 6.2, w: 11.7, h: 0.5, fontSize: 24 });
    } else {
      ar(s, "كلّما نقص الأُس بواحد نقسم على 3. أكمل الجدول:", { x: 0.8, y: 5.15, w: 11.7, h: 0.6, fontSize: 20, bold: true, color: C.text2 });
      ar(s, "ثم تحقّق بقاعدة القسمة:", { x: 8.0, y: 5.85, w: 4.5, h: 0.6, fontSize: 22, color: C.accent1 });
      mt(s, runs("3^2 ÷ 3^2 = ?", { bold: true }), { x: 4.5, y: 5.85, w: 3.5, h: 0.6, fontSize: 26, color: C.accent1, align: "right" });
    }
    return s;
  };
  zeroSlide(false);
  zeroSlide(true);

  // 14. Explanation – definition
  pres.addSection({ title: "التفسير" });
  {
    const s = content("التفسير", "ما هي القوّة؟",
      "التفسير (10 د): القوّة a^n هي جداء n عاملًا كلّ منها يساوي a (a الأساس، n الأُس). مثال: 2^5 = 2 × 2 × 2 × 2 × 2 = 32 وليس 2 × 5. نقرأ a^2 «مربّع a» لأنه مساحة مربّع طول ضلعه a، وa^3 «مكعّب a» لأنه حجم مكعّب طول حرفه a.");
    chip(s, "التفسير · 10 د", C.accent6, "FaBookOpen");
    card(s, 0.6, 1.45, 12.13, 2.1, { fill: C.text2, noShadow: true });
    ar(s, "التعريف", { x: 10.33, y: 1.55, w: 2.2, h: 0.45, fontSize: 18, bold: true, color: C.accent2 });
    mt(s, runs("a^n = a × a × … × a", { bold: true, italic: true, color: C.background1 }), { x: 0.8, y: 1.9, w: 9.0, h: 0.9, fontSize: 40 });
    ar(s, "جداء n عاملًا كلٌّ منها يساوي a", { x: 0.8, y: 2.85, w: 9.0, h: 0.5, fontSize: 18, color: C.background2, align: "center" });
    ar(s, [{ text: "a الأساس", options: { color: C.accent2, bold: true, breakLine: true } }, { text: "n الأُس", options: { color: C.accent2, bold: true } }],
      { x: 10.0, y: 2.1, w: 2.5, h: 1.2, fontSize: 18 });
    // square
    card(s, 6.83, 3.85, 5.9, 2.9, { fill: C.background2, noShadow: true });
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++)
      s.addShape(pres.shapes.RECTANGLE, { x: 10.3 + c * 0.6, y: 4.2 + r * 0.6, w: 0.6, h: 0.6, fill: { color: C.accent5, transparency: 55 }, line: { color: C.background1, width: 1.5 } });
    ar(s, "المربّع", { x: 7.0, y: 4.05, w: 3.1, h: 0.5, fontSize: 22, bold: true, color: C.accent5 });
    mt(s, runs("3^2 = 3 × 3 = 9"), { x: 7.0, y: 4.65, w: 3.1, h: 0.7, fontSize: 24, align: "right" });
    ar(s, [{ text: "نقرأ ", options: {} }, ...runs("a^2", { fontFace: MATH }), { text: " «مربّع a»", options: { bold: true } }], { x: 7.0, y: 5.45, w: 3.1, h: 0.5, fontSize: 17 });
    // cube
    card(s, 0.6, 3.85, 5.9, 2.9, { fill: C.background2, noShadow: true });
    badge(s, 4.15, 4.25, 1.8, "FaCube", C.accent6);
    ar(s, "المكعّب", { x: 0.75, y: 4.05, w: 3.2, h: 0.5, fontSize: 22, bold: true, color: C.accent6 });
    mt(s, runs("2^3 = 2 × 2 × 2 = 8"), { x: 0.75, y: 4.65, w: 3.3, h: 0.7, fontSize: 22, align: "right" });
    ar(s, [{ text: "نقرأ ", options: {} }, ...runs("a^3", { fontFace: MATH }), { text: " «مكعّب a»", options: { bold: true } }], { x: 0.75, y: 5.45, w: 3.2, h: 0.5, fontSize: 17 });
  }

  // 15. Special cases & sign
  {
    const s = content("التفسير", "حالتان خاصّتان وإشارة القوّة",
      "نعرض a^1 = a وa^0 = 1 (a ≠ 0)، مثل 7^1 = 7 و2026^0 = 1. ثم الإشارة: أساس سالب وأُس زوجي ← قوّة موجبة، أُس فردي ← قوّة سالبة. نفكّك (−2)^4 و(−2)^3 لنرى أن كل زوج من العوامل السالبة يعطي جداءً موجبًا.");
    chip(s, "التفسير · 10 د", C.accent6, "FaBookOpen");
    ar(s, "حالتان خاصّتان", { x: 6.83, y: 1.4, w: 5.9, h: 0.5, fontSize: 22, bold: true, color: C.text2 });
    [["a^1 = a", "7^1 = 7", "الأُس 1: العدد نفسه"], ["a^0 = 1  (a ≠ 0)", "2026^0 = 1", "الأُس 0: النتيجة دائمًا 1"]].forEach(([r, e, d], k) => {
      const y = 2.0 + k * 2.4;
      card(s, 6.83, y, 5.9, 2.15, { fill: C.accent1, tr: 90, line: C.accent1, ltr: 50 });
      mt(s, runs(r, { bold: true, italic: true }), { x: 6.9, y: y + 0.15, w: 5.76, h: 0.8, fontSize: 32, color: C.accent1 });
      mt(s, e, { x: 6.9, y: y + 0.9, w: 5.76, h: 0.65, fontSize: 26 });
      ar(s, d, { x: 6.9, y: y + 1.55, w: 5.76, h: 0.45, fontSize: 16, color: "4F5C6E", align: "center" });
    });
    ar(s, "إشارة القوّة عندما يكون الأساس سالبًا", { x: 0.6, y: 1.4, w: 5.9, h: 0.5, fontSize: 22, bold: true, color: C.text2 });
    [["(−2)^4 = 16", "(−2)(−2)(−2)(−2)", "أُس زوجي ← موجبة", C.accent5], ["(−2)^3 = −8", "(−2)(−2)(−2)", "أُس فردي ← سالبة", C.accent4]].forEach(([r, e, d, col], k) => {
      const y = 2.0 + k * 2.4;
      card(s, 0.6, y, 5.9, 2.15, { fill: col, tr: 90, line: col, ltr: 50 });
      mt(s, runs(r, { bold: true }), { x: 0.7, y: y + 0.15, w: 5.7, h: 0.8, fontSize: 34, color: col });
      mt(s, e, { x: 0.7, y: y + 0.9, w: 5.7, h: 0.6, fontSize: 22, color: "4F5C6E" });
      ar(s, d, { x: 0.7, y: y + 1.5, w: 5.7, h: 0.5, fontSize: 18, bold: true, color: col, align: "center" });
    });
  }

  // 16. Powers of ten
  {
    const s = content("التفسير", "قوى العشرة",
      "10^n هو العدد 1 متبوعًا بـ n أصفار. نسأل: كم صفرًا في 10^6؟ (6). مثال من الحياة: المسافة إلى القمر نحو 384 400 km، والمسافة إلى الشمس نحو 150 000 000 km.");
    chip(s, "التفسير · 10 د", C.accent6, "FaBookOpen");
    const P = [["10^1", "10"], ["10^2", "100"], ["10^3", "1 000"], ["10^4", "10 000"], ["10^5", "100 000"], ["10^6", "1 000 000"]];
    P.forEach(([p, v], k) => {
      const y = 1.45 + k * 0.8;
      mt(s, runs(p, { bold: true }), { x: 10.6, y, w: 2.1, h: 0.68, fontSize: 30, color: C.accent1, align: "right" });
      mt(s, "=", { x: 10.0, y, w: 0.6, h: 0.68, fontSize: 28 });
      const bw = 1.1 + k * 1.15;
      card(s, 10.0 - bw - 0.1, y + 0.06, bw, 0.56, { fill: C.accent2, tr: 70 - k * 8, line: C.accent2, ltr: 50, noShadow: true });
      mt(s, v, { x: 10.0 - bw - 0.1, y: y + 0.06, w: bw, h: 0.56, fontSize: 24, bold: true, color: C.text2 });
      ar(s, k === 0 ? "صفر واحد" : `${k + 1} أصفار`, { x: 0.6, y, w: 1.8, h: 0.68, fontSize: 15, color: "4F5C6E", valign: "middle", align: "left" });
    });
    card(s, 0.6, 6.35, 12.13, 0.55, { fill: C.text2, noShadow: true });
    ar(s, [...runs("10^n", { fontFace: MATH, bold: true, color: C.accent2 }), { text: " هو العدد 1 متبوعًا بـ n أصفار  ·  عدد الأصفار = الأُس", options: { color: C.background1, rtlMode: true } }],
      { x: 0.8, y: 6.35, w: 11.73, h: 0.55, fontSize: 19, align: "center", valign: "middle" });
  }

  // 17. Rules with examples
  {
    const s = content("التفسير", "القواعد مع أمثلة البطاقة",
      "نعرض القواعد الخمس (الأساس نفسه في القواعد الثلاث الأولى، والأُس نفسه في قاعدتَي قوّة الجداء وقوّة الحاصل) مع أمثلة بطاقة الشرح. يحسب التلاميذ كل مثال ويتحقّقون بالآلة الحاسبة.");
    chip(s, "التفسير · 10 د", C.accent6, "FaBookOpen");
    const head = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 }, align: "center", rtlMode: true, fontSize: 18 } });
    const m = (t, o = {}) => ({ text: runs(t, { fontFace: MATH }), options: { align: "center", fontFace: MATH, ...o } });
    const rows = [[head("مثال"), head("القاعدة"), head("الخاصّة")]];
    const data = [
      ["2^3 × 2^4 = 2^7 = 128", "a^m × a^n = a^{m+n}", "جداء قوّتين"],
      ["10^8 ÷ 10^5 = 10^3 = 1000", "a^m ÷ a^n = a^{m−n}", "قسمة قوّتين"],
      ["(3^2)^3 = 3^6 = 729", "(a^m)^n = a^{m×n}", "قوّة القوّة"],
      ["5^3 × 2^3 = 10^3 = 1000", "a^n × b^n = (a × b)^n", "قوّة الجداء"],
      ["(6 ÷ 3)^4 = 6^4 ÷ 3^4 = 16", "(a ÷ b)^n = a^n ÷ b^n", "قوّة الحاصل"],
    ];
    data.forEach(([e, r, n], k) => rows.push([m(e, { fill: { color: k % 2 ? "FFFFFF" : "EEF2F8" } }),
      m(r, { color: C.accent1, bold: true, italic: true, fill: { color: k % 2 ? "FFFFFF" : "EEF2F8" } }),
      { text: n, options: { bold: true, rtlMode: true, align: "right", color: C.text2, fill: { color: k % 2 ? "FFFFFF" : "EEF2F8" } } }]));
    s.addTable(rows, { x: 0.6, y: 1.45, w: 12.13, colW: [5.0, 4.33, 2.8], rowH: [0.6, ...Array(5).fill(0.86)], fontSize: 22, valign: "middle",
      border: { type: "solid", pt: 1, color: "DCE2E9" }, color: C.text1 });
  }

  // 18. Application – order of operations
  pres.addSection({ title: "التطبيق" });
  {
    const s = content("التطبيق", "أولويّات الحساب مع القوى",
      "التطبيق (5 د): نذكّر بأولويّات الحساب: الأقواس ثم القوى ثم الضرب والقسمة ثم الجمع والطرح. نحلّ المثال خطوة بخطوة ونسأل في كل خطوة: ما العمليّة ذات الأولويّة الآن؟");
    chip(s, "التطبيق · 5 د", C.accent5, "FaListOl");
    const steps = [["الأقواس", "( )", C.accent1], ["القوى", "a^n", C.accent6], ["الضرب والقسمة", "× ÷", C.accent3], ["الجمع والطرح", "+ −", C.accent4]];
    steps.forEach(([t, sym, col], k) => {
      const x = 12.73 - (k + 1) * 2.8 - k * 0.3;
      card(s, x, 1.45, 2.8, 1.6, { fill: col, noShadow: false });
      mt(s, runs(sym, { bold: true, color: C.background1 }), { x, y: 1.5, w: 2.8, h: 0.8, fontSize: 30 });
      ar(s, t, { x, y: 2.3, w: 2.8, h: 0.6, fontSize: 19, bold: true, color: C.background1, align: "center" });
      if (k < 3) arrowLeft(s, x - 0.3, 2.05, 0.3, 0.4, "9AA5B4");
    });
    card(s, 0.6, 3.4, 12.13, 3.35, { fill: C.background2, noShadow: true });
    ar(s, "مثال", { x: 10.5, y: 3.55, w: 2.0, h: 0.45, fontSize: 18, bold: true, color: C.accent5 });
    const L = [["5^2 − 4 × 3 + 2^3", "", C.text2], ["= 25 − 4 × 3 + 8", "← القوى أوّلًا", C.accent6], ["= 25 − 12 + 8", "← ثم الضرب", C.accent3], ["= 21", "← ثم الجمع والطرح بالترتيب", C.accent4]];
    L.forEach(([e, why, col], k) => {
      const y = 3.6 + k * 0.75;
      mt(s, runs(e, { bold: k === 0 || k === 3 }), { x: 5.0, y, w: 4.5, h: 0.7, fontSize: 30, align: "left", color: k === 3 ? C.accent5 : C.text1 });
      if (why) ar(s, why, { x: 0.8, y, w: 4.1, h: 0.7, fontSize: 15, color: col, bold: true, valign: "middle" });
    });
  }

  // 19. Differentiation
  {
    const s = content("التطبيق", "لكلٍّ حسب حاجته",
      "مراعاة الفروقات الفرديّة: المتعثّرون يعتمدون على الكتابة المفكّكة وعدّ العوامل (النشاط 2) قبل تطبيق القاعدة مباشرة، مع الآلة الحاسبة للتحقّق. المتميّزون يعملون على تحدّي القمر.");
    chip(s, "الفروقات الفرديّة", C.accent5, "FaHandsHelping");
    card(s, 6.83, 1.45, 5.9, 5.3, { fill: C.accent3, tr: 90, line: C.accent3, ltr: 50 });
    badge(s, 11.6, 1.7, 0.85, "FaHandsHelping", C.accent3);
    ar(s, "دعم المتعثّرين", { x: 7.0, y: 1.8, w: 4.5, h: 0.6, fontSize: 24, bold: true, color: C.accent3 });
    ar(s, "نفكّك ثم نعدّ العوامل قبل القاعدة:", { x: 7.0, y: 2.75, w: 5.55, h: 0.5, fontSize: 17 });
    mt(s, "(2×2×2) × (2×2)", { x: 7.0, y: 3.3, w: 5.55, h: 0.7, fontSize: 28 });
    mt(s, runs("= 2^5 = 32", { bold: true, color: C.accent3 }), { x: 7.0, y: 4.0, w: 5.55, h: 0.75, fontSize: 32 });
    ar(s, "ثم نتحقّق بالآلة الحاسبة", { x: 7.0, y: 5.2, w: 5.55, h: 0.5, fontSize: 17 });
    badge(s, 9.4, 5.75, 0.8, "FaCalculator", C.accent3);
    // challenge
    card(s, 0.6, 1.45, 5.9, 5.3, { fill: C.text2 });
    badge(s, 5.4, 1.7, 0.85, "FaMoon", C.accent2);
    ar(s, "تحدّي المتميّزين", { x: 0.8, y: 1.8, w: 4.5, h: 0.6, fontSize: 24, bold: true, color: C.accent2 });
    ar(s, "سماكة الورقة نحو 0.1 ملم. لو استطعنا طيّها 42 مرّة، هل تصل سماكتها إلى القمر؟",
      { x: 0.8, y: 2.75, w: 5.5, h: 1.5, fontSize: 20, color: C.background1 });
    ar(s, [{ text: "المسافة إلى القمر نحو 384 400 كلم", options: { bold: true, color: C.accent2 } }],
      { x: 0.8, y: 4.45, w: 5.5, h: 0.6, fontSize: 18, color: C.background2 });
    ar(s, "تلميح: كل طيّة تضاعف السماكة.", { x: 0.8, y: 5.35, w: 5.5, h: 0.5, fontSize: 16, color: C.background2 });
  }

  // 20. Challenge answer
  {
    const s = content("التطبيق", "تحدّي القمر: الحلّ",
      "بعد 42 طيّة تصبح عدد الطبقات 2^42 ≈ 4.4 × 10^12. السماكة = 2^42 × 0.1 mm ≈ 439 804 651 110 mm ≈ 439 805 km، أي أكثر من المسافة إلى القمر (384 400 km). نربط ذلك بقوّة النموّ المضاعف.");
    chip(s, "تحدّي المتميّزين", C.accent5, "FaRocket");
    card(s, 0.6, 1.45, 12.13, 2.4, { fill: C.text2, noShadow: true });
    mt(s, runs("2^{42} × 0.1 mm  ≈  439 805 km", { bold: true, color: C.background1 }), { x: 0.8, y: 1.6, w: 11.73, h: 1.2, fontSize: 44 });
    ar(s, "عدد الطبقات بعد 42 طيّة مضروبًا في سماكة الطبقة الواحدة", { x: 0.8, y: 2.85, w: 11.73, h: 0.6, fontSize: 18, color: C.background2, align: "center" });
    // comparison bars
    const maxW = 9.0;
    [["سماكة الورقة", 439805, C.accent2, "439 805 km"], ["المسافة إلى القمر", 384400, "7C8797", "384 400 km"]].forEach(([t, v, col, lbl], k) => {
      const y = 4.25 + k * 1.05, w = (maxW * v) / 439805;
      ar(s, t, { x: 10.0, y, w: 2.73, h: 0.75, fontSize: 18, bold: true, valign: "middle" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.8 - w, y: y + 0.08, w, h: 0.6, rectRadius: 0.1, fill: { color: col }, line: { color: col } });
      mt(s, lbl, { x: 9.8 - w + 0.1, y: y + 0.08, w: 3.0, h: 0.6, fontSize: 20, bold: true, color: k ? C.background1 : C.text2, align: "left" });
    });
    ar(s, "نعم! تتجاوز المسافة إلى القمر", { x: 0.6, y: 6.35, w: 12.13, h: 0.5, fontSize: 22, bold: true, color: C.accent5, align: "center" });
  }

  // 21–22. Assessment – find the error
  pres.addSection({ title: "التقييم" });
  const errs = [
    ["2^3 = 6", "2^3 = 2 × 2 × 2 = 8", "القوّة ليست ضرب الأساس في الأُس"],
    ["−2^4 = 16", "−2^4 = −16", "بلا أقواس الأُس يخصّ 2 وحده"],
    ["(2 + 5)^2 = 2^2 + 5^2", "(2 + 5)^2 = 7^2 = 49", "وليس 29: الأُس لا يتوزّع على الجمع"],
    ["2^3 × 3^2 = 6^5", "2^3 × 3^2 = 8 × 9 = 72", "الأساسان والأُسّان مختلفان: نحسب كلًّا وحده"],
  ];
  const errSlide = (solved) => {
    const s = content("التقييم", solved ? "اكتشف الخطأ: التصحيح" : "انتبه! اكتشف الخطأ وصحّحه",
      solved ? "نناقش كل خطأ ونطلب من تلميذ أن يشرح سبب الخطأ بكلماته قبل عرض التصحيح. نربط كل خطأ بالقاعدة المناسبة."
        : "النشاط التقييمي (مناقشة وحوار): تعرض كل مجموعة رأيها في كل عبارة: صحيحة أم خاطئة؟ ولماذا؟ ثم تكتب التصحيح.");
    chip(s, "النشاط التقييمي", C.accent4, "FaExclamationTriangle");
    errs.forEach(([w, c, why], k) => {
      const col = k % 2, row = Math.floor(k / 2);
      const x = 12.73 - (col + 1) * 5.9 - col * 0.33, y = 1.45 + row * 2.75;
      card(s, x, y, 5.9, 2.5, { fill: C.background1, line: "DCE2E9" });
      num(s, x + 5.25, y + 0.2, 0.5, k + 1, C.accent4);
      mt(s, runs(w + (solved ? "" : "  ؟")), { x: x + 0.2, y: y + 0.15, w: 4.9, h: 0.8, fontSize: 30, bold: true,
        color: C.accent4, strike: solved ? "sngStrike" : undefined });
      if (solved) {
        mt(s, runs(c, { bold: true }), { x: x + 0.2, y: y + 0.95, w: 5.5, h: 0.75, fontSize: 26, color: C.accent5 });
        ar(s, why, { x: x + 0.2, y: y + 1.75, w: 5.5, h: 0.55, fontSize: 16, color: "4F5C6E", align: "center" });
      } else {
        ar(s, "صحيحة أم خاطئة؟ لماذا؟", { x: x + 0.2, y: y + 1.05, w: 5.5, h: 0.5, fontSize: 17, color: "4F5C6E", align: "center" });
        mt(s, "التصحيح: ……………………", { x: x + 0.2, y: y + 1.6, w: 5.5, h: 0.6, fontSize: 18, color: "9AA5B4" });
      }
    });
    return s;
  };
  errSlide(false);
  errSlide(true);

  // 23. Homework
  pres.addSection({ title: "الختام" });
  {
    const s = content("الختام", "الواجب البيتي",
      "الواجب: إعادة جدول لغز الأُس صفر بالأساس 5 (5^4 = 625، 5^3 = 125، 5^2 = 25، 5^1 = 5، 5^0 = 1)، والتحقّق بقاعدة القسمة 5^2 ÷ 5^2 = 5^0 = 1: النتيجة لا تتغيّر. وإكمال جدول طيّ الورقة حتى 10 طيّات لمن لم يُنهِه في الصف.");
    chip(s, "الواجب البيتي", C.accent1, "FaHome");
    card(s, 0.6, 1.45, 12.13, 3.35, { fill: C.background2, noShadow: true });
    num(s, 12.05, 1.65, 0.5, 1, C.accent1);
    ar(s, "أعد جدول «لغز الأُس صفر» بالأساس 5 بدلًا من 3:", { x: 2.0, y: 1.6, w: 9.9, h: 0.6, fontSize: 19, bold: true });
    ["5^4", "5^3", "5^2", "5^1", "5^0"].forEach((p, k) => {
      const x = 10.35 - k * 2.3;
      card(s, x, 2.4, 2.0, 1.25, { fill: C.background1, line: "DCE2E9", noShadow: true });
      mt(s, runs(p + " = …", { bold: true }), { x, y: 2.4, w: 2.0, h: 1.25, fontSize: 26, color: C.text2 });
      if (k < 4) mt(s, "÷5", { x: x - 0.33, y: 2.65, w: 0.36, h: 0.5, fontSize: 14, bold: true, color: C.accent4 });
    });
    ar(s, "ثم تحقّق بقاعدة القسمة:", { x: 8.4, y: 3.95, w: 3.5, h: 0.6, fontSize: 20, color: C.accent1 });
    mt(s, runs("5^2 ÷ 5^2", { bold: true }), { x: 6.4, y: 3.95, w: 2.0, h: 0.6, fontSize: 24, color: C.accent1 });
    ar(s, "هل تتغيّر النتيجة؟", { x: 3.4, y: 3.95, w: 3.0, h: 0.6, fontSize: 20, color: C.accent1 });
    card(s, 0.6, 5.1, 12.13, 1.6, { fill: C.background2, noShadow: true });
    num(s, 12.05, 5.3, 0.5, 2, C.accent1);
    ar(s, "أكمل جدول طيّ الورقة حتى 10 طيّات (لمن لم يُنهِه في الصف).", { x: 2.4, y: 5.25, w: 9.5, h: 0.6, fontSize: 19, bold: true });
    ar(s, "تذكّر: كل طيّة تضاعف عدد الطبقات.", { x: 2.4, y: 5.85, w: 9.5, h: 0.5, fontSize: 17, color: "4F5C6E" });
    badge(s, 0.9, 5.3, 1.1, "FaLayerGroup", C.accent3);
  }

  // 24. Closing summary
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "الختام" });
    ar(s, "ماذا تعلّمنا اليوم؟", { x: 2.0, y: 0.55, w: 10.53, h: 0.9, fontSize: 40, bold: true, color: C.background1, valign: "middle" });
    const K = [
      ["القوّة اختصار للضرب المتكرّر", "2^5 = 2 × 2 × 2 × 2 × 2 = 32"],
      ["الأساس نفسه: نجمع الأُسّين في الجداء", "a^m × a^n = a^{m+n}"],
      ["كل عدد غير معدوم أُس صفر يساوي 1", "a^0 = 1"],
      ["قوى العشرة: 1 متبوعًا بـ n أصفار", "10^6 = 1 000 000"],
    ];
    K.forEach(([t, m], k) => {
      const col = k % 2, row = Math.floor(k / 2);
      const x = 12.53 - (col + 1) * 5.7 - col * 0.33, y = 1.85 + row * 2.45;
      card(s, x, y, 5.7, 2.15, { fill: C.accent1, noShadow: true });
      ar(s, t, { x: x + 0.2, y: y + 0.2, w: 5.3, h: 0.6, fontSize: 19, bold: true, color: C.accent2 });
      mt(s, runs(m, { bold: true, color: C.background1 }), { x: x + 0.2, y: y + 0.9, w: 5.3, h: 1.0, fontSize: 30 });
    });
    s.addImage({ data: ICON.FaFlagCheckered, x: 0.8, y: 0.65, w: 0.6, h: 0.6 });
    s.addNotes("خلاصة الحصّة: نعود إلى الأهداف ونسأل التلاميذ أيّها تحقّق. نذكّر بالواجب البيتي.");
  }

  await pres.writeFile({ fileName: OUT });
  const applyThemePath = process.argv[2];
  if (applyThemePath) await require(applyThemePath).applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
