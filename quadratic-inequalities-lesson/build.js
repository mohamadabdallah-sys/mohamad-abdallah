// Builds "المتراجحات من الدرجة الثانية" lesson deck.
// Run: NODE_PATH=<dir with pptxgenjs, react-icons, react, react-dom, sharp> node build.js <path to pptx skill apply_theme.js>
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const APPLY_THEME = process.argv[2];
const OUT = path.join(__dirname, "المتراجحات-من-الدرجة-الثانية.pptx");

const THEME = {
  name: "Quadratic Inequalities",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1D2B36", lt1: "FFFFFF", dk2: "0B3C49", lt2: "EEF5F4",
    accent1: "1B998B", accent2: "F46036", accent3: "2E9E5B",
    accent4: "E0A100", accent5: "7B4BB7", accent6: "5C7480",
    hlink: "1B998B", folHlink: "7B4BB7",
  },
};
const H = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "المتراجحات من الدرجة الثانية";
pres.subject = "رياضيات";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// Wrap a math expression so it stays left-to-right inside Arabic text.
const m = (s) => "‪" + s + "‬";
const AR = { rtlMode: true, lang: "ar-LB", align: "right" };

async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE",
  background: { color: H.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.3, w: 11.7, h: 1.4, fontSize: 48, bold: true, color: C.background1, align: "right", valign: "middle", rtlMode: true }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.8, w: 11.7, h: 0.9, fontSize: 22, color: C.background2, align: "right", valign: "top", rtlMode: true }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CLOSING",
  background: { color: H.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 0.45, w: 11.7, h: 1.0, fontSize: 40, bold: true, color: C.background1, align: "right", valign: "middle", rtlMode: true }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: H.lt1 },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 4.2, y: 0.35, w: 8.53, h: 0.85, fontSize: 32, bold: true, color: C.text2, align: "right", valign: "middle", rtlMode: true }, text: "" } },
  ],
  slideNumber: { x: 0.45, y: 6.95, w: 0.5, h: 0.35, fontSize: 11, color: C.accent6 },
});

// ---------- helpers ----------
function newSlide(section, title, phase, phaseColor) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(title, { placeholder: "title", ...AR });
  if (phase) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 0.55, w: 3.2, h: 0.48, rectRadius: 0.24, fill: { color: phaseColor || C.accent1 }, line: { type: "none" }, objectName: "phase-pill" });
    s.addText(phase, { x: 0.6, y: 0.55, w: 3.2, h: 0.48, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", rtlMode: true, lang: "ar-LB", isTextBox: true, margin: 0, objectName: "phase-text" });
  }
  return s;
}

function card(s, x, y, w, h, fill, name) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill || C.background2 }, line: { type: "none" }, shadow: { type: "outer", color: "9AB3B0", blur: 6, offset: 2, angle: 90, opacity: 0.35 }, objectName: name || "card" });
}

function iconCircle(s, data, x, y, d, fill) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: "icon-circle" });
  s.addImage({ data, x: x + d * 0.24, y: y + d * 0.24, w: d * 0.52, h: d * 0.52, objectName: "icon" });
}

function numberBadge(s, n, x, y, d, fill) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: "number-badge" });
  s.addText(String(n), { x, y, w: d, h: d, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
}

function txt(s, text, o) {
  s.addText(text, { isTextBox: true, fontSize: 16, color: C.text1, valign: "top", ...AR, ...o });
}

// Math line, left-to-right, aligned right to sit under Arabic text.
function mathTxt(s, text, o) {
  s.addText(text, { isTextBox: true, fontSize: 18, color: C.text2, valign: "middle", align: "right", rtlMode: false, ...o });
}

// Sign table (left-to-right as written in class).
function signTable(s, rows, x, y, colW, rowH, headFill) {
  const data = rows.map((r, i) =>
    r.map((cell, j) => {
      const isHead = i === 0;
      const isSign = cell === "+" || cell === "−";
      return {
        text: cell,
        options: {
          bold: isHead || j === 0 || isSign,
          color: isHead ? C.background1 : cell === "+" ? C.accent3 : cell === "−" ? C.accent2 : C.text1,
          fill: { color: isHead ? headFill || C.text2 : C.background1 },
          fontSize: isSign ? 20 : 15,
          align: "center",
          valign: "middle",
          rtlMode: false,
        },
      };
    })
  );
  s.addTable(data, { x, y, colW, rowH, border: { type: "solid", pt: 1, color: "B8CBC9" }, margin: 0.03 });
}

(async () => {
  const ic = {
    target: await icon(fa.FaBullseye, "FFFFFF"),
    bulb: await icon(fa.FaLightbulb, "FFFFFF"),
    search: await icon(fa.FaSearch, "FFFFFF"),
    users: await icon(fa.FaUsers, "FFFFFF"),
    chart: await icon(fa.FaChartLine, "FFFFFF"),
    table: await icon(fa.FaTable, "FFFFFF"),
    check: await icon(fa.FaCheck, "FFFFFF"),
    times: await icon(fa.FaTimes, "FFFFFF"),
    flag: await icon(fa.FaFlagCheckered, "FFFFFF"),
    hand: await icon(fa.FaHandsHelping, "FFFFFF"),
    star: await icon(fa.FaStar, "FFFFFF"),
    rocket: await icon(fa.FaRocket, "FFFFFF"),
    seed: await icon(fa.FaSeedling, "FFFFFF"),
    clock: await icon(fa.FaClock, "FFFFFF"),
    ticket: await icon(fa.FaTicketAlt, "FFFFFF"),
    book: await icon(fa.FaBookOpen, "FFFFFF"),
    pen: await icon(fa.FaPencilAlt, "FFFFFF"),
    bubble: await icon(fa.FaComments, "FFFFFF"),
    seedG: await icon(fa.FaSeedling, H.accent3),
    chartY: await icon(fa.FaChartLine, H.accent4),
    rocketP: await icon(fa.FaRocket, H.accent5),
    tealParabola: await icon(fa.FaChartLine, H.accent1, 512),
  };

  // ===== 1. Title =====
  pres.addSection({ title: "مقدمة" });
  {
    const s = pres.addSlide({ masterName: "TITLE", sectionTitle: "مقدمة" });
    s.addText("المتراجحات من الدرجة الثانية", { placeholder: "title", ...AR });
    s.addText("إشارة ثلاثي الحدود ax² + bx + c وكيفية حل المتراجحة", { placeholder: "body", ...AR });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 5.2, w: 5.6, h: 0.6, rectRadius: 0.3, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "tag" });
    s.addText("نشاط تمهيدي · استكشاف · أمثلة · عمل مجموعات", { x: 0.8, y: 5.2, w: 5.6, h: 0.6, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, rtlMode: true });
    s.addImage({ data: ic.tealParabola, x: 0.9, y: 0.7, w: 1.3, h: 1.3, objectName: "motif-icon" });
    s.addNotes("مدة الحصة المقترحة: حصتان (2 × 50 دقيقة). المكتسبات القبلية: حل معادلة من الدرجة الثانية باستعمال المميّز Δ، وإشارة ثنائي الحد ax + b.");
  }

  // ===== 2. Objectives =====
  {
    const s = newSlide("مقدمة", "أهداف الدرس", "في نهاية الدرس", C.accent6);
    const goals = [
      [ic.search, C.accent1, "أربط إشارة ثلاثي الحدود بموقع منحنيه بالنسبة لمحور الفواصل"],
      [ic.table, C.accent2, "أحدّد إشارة " + m("ax² + bx + c") + " حسب إشارة المميّز Δ وإشارة a"],
      [ic.pen, C.accent3, "أحلّ متراجحة من الدرجة الثانية وأكتب مجموعة الحلول على شكل مجالات"],
      [ic.rocket, C.accent5, "أوظّف المتراجحات في حلّ مسائل حياتية ومسائل بوسيط"],
    ];
    goals.forEach(([img, col, t], i) => {
      const y = 1.65 + i * 1.25;
      card(s, 1.6, y, 10.1, 1.0, C.background2);
      iconCircle(s, img, 11.0, y + 0.12, 0.76, col);
      txt(s, t, { x: 1.9, y: y + 0.1, w: 8.9, h: 0.8, fontSize: 20, valign: "middle" });
    });
  }

  // ===== 3. Warm-up =====
  pres.addSection({ title: "النشاط التمهيدي" });
  {
    const s = newSlide("النشاط التمهيدي", "نشاط تمهيدي: نتذكّر معًا", "نشاط تمهيدي · 10 دقائق", C.accent4);
    txt(s, "يعمل كل تلميذ منفردًا، ثم نصحّح جماعيًا. تساعدنا النتائج على توزيع التلاميذ على مستويات العمل التطبيقي.", { x: 0.6, y: 1.35, w: 12.13, h: 0.6, fontSize: 16, color: C.accent6 });
    const items = [
      ["1", "حلّ المعادلة:", "x² − 5x + 6 = 0", "استعمل المميّز  Δ = b² − 4ac"],
      ["2", "احسب المميّز ثم استنتج عدد الجذور:", "2x² + x + 3 = 0", "هل للمعادلة حلول في ℝ؟"],
      ["3", "أكمل جدول إشارة ثنائي الحد:", "2x − 4", "متى يكون موجبًا؟ ومتى يكون سالبًا؟"],
    ];
    const w = 3.83, gap = 0.3;
    items.forEach(([n, q, expr, hint], i) => {
      const x = 12.73 - (i + 1) * w - i * gap; // first card on the right
      card(s, x, 2.15, w, 3.3, C.background2);
      numberBadge(s, n, x + w - 0.75, 2.35, 0.5, C.accent4);
      txt(s, q, { x: x + 0.2, y: 2.35, w: w - 1.0, h: 0.75, fontSize: 17, bold: true, valign: "middle" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.25, y: 3.3, w: w - 0.5, h: 0.8, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: "B8CBC9", width: 1 }, objectName: "expr-box" });
      s.addText(expr, { x: x + 0.25, y: 3.3, w: w - 0.5, h: 0.8, fontSize: 24, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
      txt(s, hint, { x: x + 0.2, y: 4.3, w: w - 0.4, h: 0.9, fontSize: 15, color: C.accent6, italic: true });
    });
    // sign table to complete for item 3
    txt(s, "جدول البند 3 للتعبئة:", { x: 8.2, y: 5.8, w: 4.53, h: 0.5, fontSize: 15, bold: true, valign: "middle" });
    signTable(s, [["x", "−∞", "", "…", "", "+∞"], ["2x − 4", "", "…", "0", "…", ""]], 1.6, 5.75, [1.4, 0.8, 1.3, 0.8, 1.3, 0.8], 0.42);
    s.addNotes("الحلول:\n1) Δ = 25 − 24 = 1 ، x₁ = 2 و x₂ = 3.\n2) Δ = 1 − 24 = −23 < 0 ، لا جذور حقيقية.\n3) 2x − 4 = 0 عندما x = 2 ؛ سالب قبل 2 وموجب بعد 2 (إشارة a = 2 بعد الجذر).\nالتوزيع على المستويات: من أخطأ في 1 و3 ← المستوى الأول؛ من أجاب عن 1 و3 ← المستوى الثاني؛ من أجاب عن الثلاثة بسرعة ودقة ← المستوى الثالث.");
  }

  // ===== 4. Exploration 1: the graph =====
  pres.addSection({ title: "النشاط الاستكشافي" });
  {
    const s = newSlide("النشاط الاستكشافي", "نشاط استكشافي (1): نقرأ المنحنى", "نشاط استكشافي · 15 دقيقة", C.accent1);
    const xs = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5];
    const ys = xs.map((x) => x * x - x - 6);
    card(s, 0.6, 1.4, 6.4, 5.4, C.background1);
    s.addChart(pres.charts.LINE, [{ name: "f(x) = x² − x − 6", labels: xs.map(String), values: ys }], {
      x: 0.75, y: 1.5, w: 6.1, h: 5.2,
      showTitle: true, title: "f(x) = x² − x − 6", titleFontSize: 16, titleColor: H.dk2, titleFontFace: "+mn-lt",
      lineSmooth: true, lineSize: 3, chartColors: [H.accent1], lineDataSymbol: "circle", lineDataSymbolSize: 7,
      catAxisLabelPos: "low", catAxisLabelColor: H.accent6, valAxisLabelColor: H.accent6,
      catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12, valAxisLabelFontSize: 12,
      valGridLine: { color: "DDE7E6", size: 0.75 }, catGridLine: { style: "none" },
      showLegend: false, valAxisMinVal: -8, valAxisMaxVal: 14, valAxisMajorUnit: 2,
    });
    // questions (right)
    txt(s, "لاحظ المنحنى الممثّل للدالة f ثم أجب:", { x: 7.3, y: 1.45, w: 5.43, h: 0.5, fontSize: 18, bold: true });
    const qs = [
      "ما فواصل نقاط تقاطع المنحنى مع محور الفواصل؟ ماذا تمثّل هذه القيم بالنسبة للمعادلة " + m("f(x) = 0") + "؟",
      "على أيّ مجالات يقع المنحنى فوق محور الفواصل؟ ما إشارة " + m("f(x)") + " عندها؟",
      "على أيّ مجال يقع المنحنى تحت محور الفواصل؟ ما إشارة " + m("f(x)") + " عندها؟",
      "استنتج قيم x التي تحقّق: " + m("x² − x − 6 ≤ 0"),
    ];
    qs.forEach((q, i) => {
      const y = 2.1 + i * 1.15;
      numberBadge(s, i + 1, 12.23, y + 0.05, 0.45, C.accent1);
      txt(s, q, { x: 7.3, y, w: 4.8, h: 1.05, fontSize: 15 });
    });
    s.addNotes("الإجابات المتوقعة:\n1) x = −2 و x = 3 ، وهما جذرا المعادلة x² − x − 6 = 0.\n2) المنحنى فوق محور الفواصل عندما x < −2 أو x > 3 ← f(x) > 0.\n3) تحته عندما −2 < x < 3 ← f(x) < 0.\n4) −2 ≤ x ≤ 3 أي [−2 ; 3].\nيمكن عرض الرسم على GeoGebra وتحريك المعاملات.");
  }

  // ===== 5. Exploration 2: three cases =====
  {
    const s = newSlide("النشاط الاستكشافي", "نشاط استكشافي (2): حالات المميّز", "استكشاف · عمل ثنائي", C.accent1);
    txt(s, "لكل دالة: احسب Δ، حدّد عدد نقاط التقاطع مع محور الفواصل، ثم صِف إشارة " + m("f(x)") + ".", { x: 0.6, y: 1.35, w: 12.13, h: 0.5, fontSize: 17 });
    const xs = [-2, -1, 0, 1, 2, 3, 4];
    const cases = [
      ["f₁(x) = x² − 2x − 3", xs.map((x) => x * x - 2 * x - 3), H.accent1],
      ["f₂(x) = x² − 2x + 1", xs.map((x) => x * x - 2 * x + 1), H.accent4],
      ["f₃(x) = x² − 2x + 3", xs.map((x) => x * x - 2 * x + 3), H.accent5],
    ];
    const w = 3.83, gap = 0.32;
    cases.forEach(([name, vals, col], i) => {
      const x = 12.73 - (i + 1) * w - i * gap;
      card(s, x, 2.0, w, 4.85, C.background2);
      s.addChart(pres.charts.LINE, [{ name, labels: xs.map(String), values: vals }], {
        x: x + 0.1, y: 2.05, w: w - 0.2, h: 3.0,
        showTitle: true, title: name, titleFontSize: 14, titleColor: H.dk2, titleFontFace: "+mn-lt",
        lineSmooth: true, lineSize: 2.5, chartColors: [col], lineDataSymbol: "none",
        catAxisLabelPos: "low", catAxisLabelColor: H.accent6, valAxisLabelColor: H.accent6,
        catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 10, valAxisLabelFontSize: 10,
        valGridLine: { color: "DDE7E6", size: 0.5 }, catGridLine: { style: "none" },
        showLegend: false, valAxisMinVal: -4, valAxisMaxVal: 12, valAxisMajorUnit: 4,
      });
      const rows = [m("Δ = ……"), "عدد نقاط التقاطع: ……", "إشارة " + m("f(x)") + ": ……………"];
      rows.forEach((r, k) => {
        txt(s, r, { x: x + 0.25, y: 5.15 + k * 0.52, w: w - 0.5, h: 0.48, fontSize: 15, valign: "middle", bold: k === 0 });
      });
    });
    s.addNotes("الإجابات:\nf₁: Δ = 16 > 0 ، نقطتا تقاطع (x = −1 و x = 3) ، f₁ موجبة خارج الجذرين وسالبة بينهما.\nf₂: Δ = 0 ، نقطة تماس واحدة x = 1 ، f₂ موجبة ما عدا عند x = 1 حيث تنعدم.\nf₃: Δ = −8 < 0 ، لا تقاطع ، f₃ موجبة دائمًا.\nسؤال إضافي للنقاش: ماذا يتغيّر لو كان a < 0؟ (ينقلب المنحنى نحو الأسفل فتنقلب الإشارات).");
  }

  // ===== 6. The rule =====
  pres.addSection({ title: "بناء المفهوم" });
  {
    const s = newSlide("بناء المفهوم", "القاعدة: إشارة " + m("ax² + bx + c"), "استنتاج · نعمّم", C.accent2);
    const rows = [
      ["Δ > 0", "جذران x₁ < x₂", [["x", "−∞", "", "x₁", "", "x₂", "", "+∞"], ["P(x)", "", "مثل a", "0", "عكس a", "0", "مثل a", ""]], "إشارة a خارج الجذرين، وعكس إشارة a بينهما", C.accent1],
      ["Δ = 0", "جذر مضاعف x₀", [["x", "−∞", "", "x₀", "", "+∞"], ["P(x)", "", "مثل a", "0", "مثل a", ""]], "إشارة a لكل " + m("x ≠ x₀") + " ، وتنعدم عند " + m("x₀"), C.accent4],
      ["Δ < 0", "لا جذور", [["x", "−∞", "", "+∞"], ["P(x)", "", "مثل a", ""]], "إشارة a دائمًا لكل x من ℝ", C.accent5],
    ];
    rows.forEach(([cond, roots, table, rule, col], i) => {
      const y = 1.45 + i * 1.8;
      card(s, 0.6, y, 12.13, 1.6, C.background2);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.35, y: y + 0.2, w: 2.15, h: 1.2, rectRadius: 0.12, fill: { color: col }, line: { type: "none" }, objectName: "case-badge" });
      s.addText([
        { text: cond, options: { fontSize: 24, bold: true, breakLine: true, rtlMode: false } },
        { text: roots, options: { fontSize: 14, rtlMode: true } },
      ], { x: 10.35, y: y + 0.2, w: 2.15, h: 1.2, color: C.background1, align: "center", valign: "middle", isTextBox: true, margin: 0 });
      const n = table[0].length;
      const colW = n === 8 ? [0.8, 0.55, 0.95, 0.5, 0.95, 0.5, 0.95, 0.55] : n === 6 ? [0.8, 0.6, 1.4, 0.6, 1.4, 0.6] : [0.8, 0.9, 2.9, 0.9];
      const tw = colW.reduce((a, b) => a + b, 0);
      signTable(s, table, 4.35 + (5.75 - tw) / 2, y + 0.38, colW, 0.42, col);
      txt(s, rule, { x: 0.85, y: y + 0.2, w: 3.3, h: 1.2, fontSize: 16, bold: true, valign: "middle" });
    });
    s.addNotes("نلخّص ما استنتجه التلاميذ من النشاط الاستكشافي. التركيز على عبارة: «إشارة a دائمًا، إلا بين الجذرين».");
  }

  // ===== 7. Method =====
  {
    const s = newSlide("بناء المفهوم", "كيف نحلّ متراجحة من الدرجة الثانية؟", "طريقة الحل · 4 خطوات", C.accent2);
    const steps = [
      [ic.pen, "نرتّب المتراجحة", "ننقل جميع الحدود إلى طرف واحد لنحصل على الشكل:", [{ text: "ax² + bx + c ≥ 0", options: { breakLine: true } }, { text: "(أو ≤ ، > ، <)", options: { fontSize: 13, bold: false } }]],
      [ic.chart, "نحسب المميّز", "نحسب Δ ثم الجذور إن وُجدت:", [{ text: "Δ = b² − 4ac", options: { breakLine: true } }, { text: "x = (−b ± √Δ) / 2a" }]],
      [ic.table, "ننشئ جدول الإشارة", "نطبّق القاعدة حسب إشارة Δ وإشارة a", [{ text: "Δ > 0 ، Δ = 0 ، Δ < 0", options: { breakLine: true } }, { text: "+ / −", options: { color: C.accent2 } }]],
      [ic.check, "نكتب مجموعة الحلول", "نختار المجالات التي تحقّق رمز المتراجحة", [{ text: "≤ , ≥  →  [ ]", options: { breakLine: true } }, { text: "< , >  →  ] [" }]],
    ];
    const w = 2.84, gap = 0.25;
    steps.forEach(([img, head, body, expr], i) => {
      const x = 12.73 - (i + 1) * w - i * gap;
      card(s, x, 1.55, w, 4.7, C.background2);
      iconCircle(s, img, x + w / 2 - 0.45, 1.8, 0.9, C.accent2);
      numberBadge(s, i + 1, x + w - 0.6, 1.7, 0.42, C.text2);
      s.addText(head, { x: x + 0.15, y: 2.85, w: w - 0.3, h: 0.55, fontSize: 19, bold: true, color: C.text2, align: "center", valign: "middle", rtlMode: true, isTextBox: true });
      txt(s, body, { x: x + 0.2, y: 3.45, w: w - 0.4, h: 1.25, fontSize: 15 });
      if (expr) {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.15, y: 4.85, w: w - 0.3, h: 1.15, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: "B8CBC9", width: 1 }, objectName: "expr-box" });
        s.addText(expr, { x: x + 0.15, y: 4.85, w: w - 0.3, h: 1.15, fontSize: 15, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
      }
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 6.45, w: 12.13, h: 0.6, rectRadius: 0.3, fill: { color: C.text2 }, line: { type: "none" }, objectName: "key-tip" });
    txt(s, "تذكّر: في المتراجحة نبحث عن مجموعة من القيم (مجال أو اتحاد مجالات)، وليس عن قيمة واحدة.", { x: 0.9, y: 6.45, w: 11.5, h: 0.6, fontSize: 16, bold: true, color: C.background1, valign: "middle" });
  }

  // ===== 8. Worked example 1 =====
  pres.addSection({ title: "أمثلة محلولة" });
  {
    const s = newSlide("أمثلة محلولة", "مثال محلول (1): حالة " + m("Δ > 0"), "أمثلة محلولة", C.accent3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.1, y: 1.4, w: 5.63, h: 0.75, rectRadius: 0.12, fill: { color: C.text2 }, line: { type: "none" }, objectName: "problem" });
    s.addText([
      { text: "حلّ في ℝ المتراجحة:   ", options: { rtlMode: true } },
      { text: m("x² − x − 6 ≤ 0") },
    ], { x: 7.1, y: 1.4, w: 5.63, h: 0.75, fontSize: 22, bold: true, color: C.background1, align: "right", valign: "middle", isTextBox: true, rtlMode: true, margin: [0, 18, 0, 18] });
    const steps = [
      ["المعاملات:", "a = 1 > 0 ،  b = −1 ،  c = −6"],
      ["المميّز:", "Δ = (−1)² − 4(1)(−6) = 1 + 24 = 25 > 0"],
      ["الجذران:", "x₁ = (1 − 5)/2 = −2  ،  x₂ = (1 + 5)/2 = 3"],
      ["الإشارة:", null],
    ];
    steps.forEach(([lab, expr], i) => {
      const y = 2.4 + i * 1.08;
      numberBadge(s, i + 1, 12.28, y, 0.42, C.accent3);
      txt(s, lab, { x: 10.0, y: y - 0.04, w: 2.15, h: 0.5, fontSize: 17, bold: true, valign: "middle" });
      if (expr) mathTxt(s, expr, { x: 6.9, y: y + 0.45, w: 5.25, h: 0.5, fontSize: 17 });
      else txt(s, "بما أنّ " + m("a > 0") + " فإنّ " + m("P(x)") + " سالبة بين الجذرين فقط", { x: 6.9, y: y + 0.45, w: 5.25, h: 0.5, fontSize: 16, valign: "middle" });
    });
    // left: sign table + solution
    card(s, 0.6, 1.4, 5.9, 5.35, C.background2);
    txt(s, "جدول الإشارة", { x: 0.8, y: 1.55, w: 5.5, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
    signTable(s, [["x", "−∞", "", "−2", "", "3", "", "+∞"], ["x² − x − 6", "", "+", "0", "−", "0", "+", ""]], 0.85, 2.2, [1.4, 0.5, 0.7, 0.5, 0.7, 0.5, 0.7, 0.5], 0.5);
    txt(s, "نختار المجال حيث " + m("P(x) ≤ 0") + " ، والجذران داخلان لأنّ الرمز " + m("≤"), { x: 0.85, y: 3.4, w: 5.4, h: 0.9, fontSize: 15 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.1, y: 4.5, w: 4.9, h: 1.1, rectRadius: 0.15, fill: { color: C.accent3 }, line: { type: "none" }, objectName: "solution" });
    s.addText("S = [ −2 ; 3 ]", { x: 1.1, y: 4.5, w: 4.9, h: 1.1, fontSize: 32, bold: true, color: C.background1, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
    txt(s, "ولو كانت المتراجحة " + m("x² − x − 6 > 0") + " لكان:", { x: 0.85, y: 5.75, w: 5.4, h: 0.45, fontSize: 14, color: C.accent6, italic: true });
    mathTxt(s, "S = ]−∞ ; −2[ ∪ ]3 ; +∞[", { x: 0.85, y: 6.2, w: 5.4, h: 0.45, fontSize: 16, bold: true, color: C.accent6, align: "center" });
  }

  // ===== 9. Worked examples 2 & 3 =====
  {
    const s = newSlide("أمثلة محلولة", "مثالان محلولان: حالتا " + m("Δ < 0") + " و " + m("Δ = 0"), "أمثلة محلولة", C.accent3);
    const ex = [
      ["مثال (2)", "−2x² + 3x − 5 < 0", ["a = −2 < 0", "Δ = 9 − 40 = −31 < 0"], "لا جذور، فالعبارة تأخذ إشارة a دائمًا: سالبة لكل x", "S = ℝ", "ولو كانت " + m("−2x² + 3x − 5 > 0") + " لكان " + m("S = ∅"), C.accent5],
      ["مثال (3)", "x² − 6x + 9 > 0", ["a = 1 > 0", "Δ = 36 − 36 = 0  ،  x₀ = 3"], "موجبة لكل " + m("x ≠ 3") + " ، وتنعدم عند " + m("x = 3"), "S = ℝ − {3}", "ولو كانت " + m("x² − 6x + 9 < 0") + " لكان " + m("S = ∅"), C.accent4],
    ];
    const w = 5.9, gap = 0.33;
    ex.forEach(([lab, expr, lines, concl, sol, variant, col], i) => {
      const x = 12.73 - (i + 1) * w - i * gap;
      card(s, x, 1.45, w, 5.4, C.background2);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.25, y: 1.65, w: w - 0.5, h: 0.8, rectRadius: 0.12, fill: { color: col }, line: { type: "none" }, objectName: "problem" });
      s.addText([
        { text: lab + ":   ", options: { rtlMode: true } },
        { text: m(expr) },
      ], { x: x + 0.25, y: 1.65, w: w - 0.5, h: 0.8, fontSize: 22, bold: true, color: C.background1, align: "right", valign: "middle", isTextBox: true, rtlMode: true, margin: [0, 16, 0, 16] });
      lines.forEach((l, k) => mathTxt(s, l, { x: x + 0.3, y: 2.7 + k * 0.6, w: w - 0.6, h: 0.55, fontSize: 18 }));
      txt(s, concl, { x: x + 0.3, y: 3.95, w: w - 0.6, h: 0.8, fontSize: 16, bold: true });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 1.0, y: 4.85, w: w - 2.0, h: 0.95, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: col, width: 2 }, objectName: "solution" });
      s.addText(sol, { x: x + 1.0, y: 4.85, w: w - 2.0, h: 0.95, fontSize: 28, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
      txt(s, variant, { x: x + 0.3, y: 6.0, w: w - 0.6, h: 0.6, fontSize: 14, italic: true, color: C.accent6, align: "center" });
    });
  }

  // ===== 10. Common mistakes =====
  {
    const s = newSlide("أمثلة محلولة", "أخطاء شائعة نتجنّبها", "انتبه!", C.accent2);
    const mistakes = [
      ["الحلّ قبل الترتيب", "لا نحسب Δ قبل نقل كل الحدود إلى طرف واحد.", "3x² ≤ 2x + 1  ⟺  3x² − 2x − 1 ≤ 0"],
      ["القسمة على x", "x قد تكون سالبة فينقلب الرمز؛ لذلك لا نقسم على عبارة مجهولة الإشارة.", "x² > 3x  ⟺  x² − 3x > 0  ⟺  x(x − 3) > 0"],
      ["الخلط بين الأقواس", "الرمز الواسع يُدخل الجذور في الحل، والرمز التامّ يستثنيها. واللانهاية دائمًا مفتوحة.", "[ −2 ; 3 ]      ]−∞ ; −2[ ∪ ]3 ; +∞["],
      ["هل " + m("Δ < 0") + " تعني انعدام الحل؟", "ليس دائمًا! مجموعة الحلول إمّا ℝ وإمّا ∅ حسب إشارة a ورمز المتراجحة.", "x² + 1 > 0  ⟹  S = ℝ"],
    ];
    const w = 5.9, h = 2.55;
    mistakes.forEach(([head, body, expr], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = col === 0 ? 6.83 : 0.6, y = 1.45 + row * (h + 0.3);
      card(s, x, y, w, h, C.background2);
      iconCircle(s, ic.times, x + w - 0.85, y + 0.2, 0.62, C.accent2);
      txt(s, head, { x: x + 0.25, y: y + 0.2, w: w - 1.2, h: 0.62, fontSize: 19, bold: true, color: C.text2, valign: "middle" });
      txt(s, body, { x: x + 0.25, y: y + 0.9, w: w - 0.5, h: 0.8, fontSize: 15 });
      mathTxt(s, expr, { x: x + 0.25, y: y + 1.75, w: w - 0.5, h: 0.6, fontSize: 16, bold: true, color: C.accent1, align: "center" });
    });
  }

  // ===== 11. Group work organisation =====
  pres.addSection({ title: "العمل التطبيقي" });
  {
    const s = newSlide("العمل التطبيقي", "عمل تطبيقي متعدّد المستويات", "عمل تطبيقي · 20 دقيقة", C.accent5);
    // right: organisation
    card(s, 6.6, 1.45, 6.13, 5.4, C.background2);
    txt(s, "تنظيم العمل", { x: 6.85, y: 1.6, w: 5.63, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
    const org = [
      [ic.users, "مجموعات من 4 تلاميذ، تُشكَّل حسب نتائج النشاط التمهيدي"],
      [ic.hand, "الأدوار: قائد (الوقت) · كاتب · مدقّق · عارض"],
      [ic.clock, "20 دقيقة عمل، ثم 10 دقائق عرض ومناقشة"],
      [ic.star, "المجموعة التي تنهي باكرًا تحلّ «التحدّي» أو تساعد مجموعة أخرى"],
      [ic.bubble, "«بطاقة مساعدة» متوفّرة عند المعلّم لمن يحتاجها"],
    ];
    org.forEach(([img, t], i) => {
      const y = 2.25 + i * 0.9;
      iconCircle(s, img, 11.9, y, 0.6, C.accent5);
      txt(s, t, { x: 6.85, y: y - 0.08, w: 4.9, h: 0.78, fontSize: 15, valign: "middle" });
    });
    // left: levels
    const lv = [
      [ic.seedG, "المستوى الأول · أساسي", "تطبيق مباشر مع جدول إشارة جاهز وتلميحات", C.accent3],
      [ic.chartY, "المستوى الثاني · متوسط", "جميع حالات Δ وترتيب المتراجحة قبل الحل", C.accent4],
      [ic.rocketP, "المستوى الثالث · متقدّم", "مسألة حياتية، وسيط m، ومتراجحة بتغيير متغيّر", C.accent5],
    ];
    lv.forEach(([img, head, body, col], i) => {
      const y = 1.45 + i * 1.86;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 5.7, h: 1.62, rectRadius: 0.12, fill: { color: col }, line: { type: "none" }, objectName: "level-card" });
      iconCircle(s, img, 5.25, y + 0.25, 0.8, C.background1);
      txt(s, head, { x: 0.85, y: y + 0.2, w: 4.25, h: 0.55, fontSize: 19, bold: true, color: C.background1, valign: "middle" });
      txt(s, body, { x: 0.85, y: y + 0.78, w: 4.25, h: 0.7, fontSize: 15, color: C.background1 });
    });
    s.addNotes("مراعاة الفروق الفردية: البطاقات الثلاث تتناول المفهوم نفسه بمستويات تعقيد مختلفة. يمكن نقل التلميذ إلى مستوى أعلى عند إنهائه بطاقته بنجاح. المعلّم يتجوّل ويطرح أسئلة موجِّهة دون إعطاء الحل.");
  }

  // ===== 12. Level 1 =====
  {
    const s = newSlide("العمل التطبيقي", "بطاقة المستوى الأول · أساسي", "المستوى الأول", C.accent3);
    txt(s, "حلّ في ℝ كلًّا من المتراجحات الآتية، واكتب مجموعة الحلول:", { x: 0.6, y: 1.35, w: 12.13, h: 0.5, fontSize: 18, bold: true });
    const ex = ["(x − 1)(x + 4) > 0", "x² − 9 ≤ 0", "x² − 4x + 3 < 0"];
    ex.forEach((e, i) => {
      const y = 2.05 + i * 1.12;
      card(s, 7.0, y, 5.73, 0.92, C.background2);
      numberBadge(s, ["أ", "ب", "ج"][i], 12.08, y + 0.2, 0.52, C.accent3);
      s.addText(e, { x: 7.2, y, w: 4.7, h: 0.92, fontSize: 24, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
    });
    // help card
    card(s, 0.6, 2.05, 6.1, 4.75, "E7F4EC");
    iconCircle(s, ic.bulb, 5.85, 2.2, 0.6, C.accent3);
    txt(s, "بطاقة مساعدة للبند (أ)", { x: 0.85, y: 2.2, w: 4.9, h: 0.6, fontSize: 18, bold: true, color: C.text2, valign: "middle" });
    txt(s, "أكمل جدول إشارة الجداء مستعينًا بإشارة ثنائي الحد:", { x: 0.85, y: 2.9, w: 5.6, h: 0.5, fontSize: 15 });
    signTable(s, [
      ["x", "−∞", "", "−4", "", "1", "", "+∞"],
      ["x + 4", "", "−", "0", "…", "", "…", ""],
      ["x − 1", "", "…", "", "…", "0", "+", ""],
      ["الجداء", "", "…", "0", "…", "0", "…", ""],
    ], 0.85, 3.5, [1.1, 0.55, 0.65, 0.55, 0.65, 0.55, 0.65, 0.55], 0.42);
    txt(s, "تلميح (ب): حلّل إلى جداء عاملين", { x: 0.85, y: 5.35, w: 5.6, h: 0.42, fontSize: 15, color: C.accent6 });
    mathTxt(s, "x² − 9 = (x − 3)(x + 3)", { x: 0.85, y: 5.75, w: 5.6, h: 0.42, fontSize: 15, color: C.accent6 });
    txt(s, "تلميح (ج): ابدأ بحساب Δ، ثم طبّق القاعدة", { x: 0.85, y: 6.2, w: 5.6, h: 0.42, fontSize: 15, color: C.accent6 });
    s.addNotes("الحلول:\nأ) جذران −4 و 1 ، a = 1 > 0 ⟵ S = ]−∞ ; −4[ ∪ ]1 ; +∞[.\nب) جذران −3 و 3 ⟵ S = [−3 ; 3].\nج) Δ = 16 − 12 = 4 ، جذران 1 و 3 ⟵ S = ]1 ; 3[.");
  }

  // ===== 13. Level 2 =====
  {
    const s = newSlide("العمل التطبيقي", "بطاقة المستوى الثاني · متوسط", "المستوى الثاني", C.accent4);
    txt(s, "حلّ في ℝ كلًّا من المتراجحات الآتية (انتبه إلى إشارة Δ وإشارة a):", { x: 0.6, y: 1.35, w: 12.13, h: 0.5, fontSize: 18, bold: true });
    const ex = ["2x² − 5x − 3 ≥ 0", "x² + x + 1 > 0", "−x² + 4x − 4 ≥ 0", "3x² ≤ 2x + 1"];
    const w = 5.9, h = 1.5;
    ex.forEach((e, i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = col === 0 ? 6.83 : 0.6, y = 2.05 + row * (h + 0.3);
      card(s, x, y, w, h, C.background2);
      numberBadge(s, ["أ", "ب", "ج", "د"][i], x + w - 0.75, y + 0.48, 0.55, C.accent4);
      s.addText(e, { x: x + 0.3, y, w: w - 1.2, h, fontSize: 26, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
    });
    // challenge
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.75, w: 12.13, h: 1.1, rectRadius: 0.15, fill: { color: "FBF1D3" }, line: { color: H.accent4, width: 1.5 }, objectName: "challenge" });
    iconCircle(s, ic.star, 11.9, 5.92, 0.72, C.accent4);
    s.addText([
      { text: "تحدٍّ: ", options: { bold: true, rtlMode: true } },
      { text: "اكتب متراجحة من الدرجة الثانية مجموعة حلولها:", options: { rtlMode: true } },
    ], { x: 5.3, y: 5.75, w: 6.4, h: 1.1, fontSize: 18, color: C.text1, align: "right", valign: "middle", isTextBox: true, rtlMode: true });
    mathTxt(s, "]−∞ ; 1] ∪ [4 ; +∞[", { x: 0.9, y: 5.75, w: 4.3, h: 1.1, fontSize: 22, bold: true, align: "center" });
    s.addNotes("الحلول:\nأ) Δ = 25 + 24 = 49 ، الجذران 3 و −1/2 ، a > 0 ⟵ S = ]−∞ ; −1/2] ∪ [3 ; +∞[.\nب) Δ = −3 < 0 ، a > 0 ⟵ S = ℝ.\nج) Δ = 0 ، x₀ = 2 ، a < 0 فالعبارة سالبة وتنعدم عند 2 ⟵ S = {2}.\nد) 3x² − 2x − 1 ≤ 0 ، Δ = 16 ، الجذران 1 و −1/3 ⟵ S = [−1/3 ; 1].\nالتحدي: (x − 1)(x − 4) ≥ 0 أي x² − 5x + 4 ≥ 0.");
  }

  // ===== 14. Level 3 =====
  {
    const s = newSlide("العمل التطبيقي", "بطاقة المستوى الثالث · متقدّم", "المستوى الثالث", C.accent5);
    const probs = [
      ["مسألة حياتية", "مستطيل محيطه 20 سم وطوله x. أوجد قيم x التي تجعل مساحته 21 سم² على الأقل.", "x(10 − x) ≥ 21"],
      ["وسيط", "أوجد قيم العدد الحقيقي m بحيث يكون لكل x من ℝ:", "x² + mx + 4 > 0"],
      ["تغيير متغيّر", "حلّ في ℝ المتراجحة الآتية مستعينًا بتغيير المتغيّر:", "x⁴ − 5x² + 4 < 0"],
    ];
    const w = 3.83, gap = 0.32;
    probs.forEach(([head, body, expr], i) => {
      const x = 12.73 - (i + 1) * w - i * gap;
      card(s, x, 1.45, w, 4.05, C.background2);
      numberBadge(s, i + 1, x + w - 0.72, 1.65, 0.5, C.accent5);
      txt(s, head, { x: x + 0.2, y: 1.62, w: w - 1.05, h: 0.55, fontSize: 19, bold: true, color: C.text2, valign: "middle" });
      txt(s, body, { x: x + 0.25, y: 2.35, w: w - 0.5, h: 1.6, fontSize: 16 });
      if (i === 2) mathTxt(s, "t = x²", { x: x + 0.25, y: 3.35, w: w - 0.5, h: 0.5, fontSize: 18, bold: true, color: C.accent5, align: "center" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.25, y: 4.2, w: w - 0.5, h: 0.95, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: "B8CBC9", width: 1 }, objectName: "expr-box" });
      s.addText(expr, { x: x + 0.25, y: 4.2, w: w - 0.5, h: 0.95, fontSize: 22, bold: true, color: C.text2, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.8, w: 12.13, h: 1.05, rectRadius: 0.15, fill: { color: "EEE6F7" }, line: { color: H.accent5, width: 1.5 }, objectName: "challenge" });
    iconCircle(s, ic.star, 11.9, 5.95, 0.72, C.accent5);
    s.addText([
      { text: "تحدٍّ: ", options: { bold: true, rtlMode: true } },
      { text: "حدّد قيم m ليكون للمعادلة ", options: { rtlMode: true } },
      { text: m("x² − 2mx + m + 2 = 0") },
      { text: " جذران مختلفان.", options: { rtlMode: true } },
    ], { x: 0.9, y: 5.8, w: 10.8, h: 1.05, fontSize: 18, color: C.text1, align: "right", valign: "middle", isTextBox: true, rtlMode: true });
    s.addNotes("الحلول:\n1) العرض 10 − x ، x(10 − x) ≥ 21 ⟺ x² − 10x + 21 ≤ 0 ، الجذران 3 و 7 ⟵ x ∈ [3 ; 7] (مع 0 < x < 10).\n2) a = 1 > 0 فيكفي Δ < 0: m² − 16 < 0 ⟵ m ∈ ]−4 ; 4[.\n3) t² − 5t + 4 < 0 ⟵ 1 < t < 4 ⟵ 1 < x² < 4 ⟵ S = ]−2 ; −1[ ∪ ]1 ; 2[.\nالتحدي: Δ = 4m² − 4(m + 2) = 4(m² − m − 2) = 4(m − 2)(m + 1) > 0 ⟵ m ∈ ]−∞ ; −1[ ∪ ]2 ; +∞[.");
  }

  // ===== 15. Presentation & assessment =====
  pres.addSection({ title: "التقويم والخلاصة" });
  {
    const s = newSlide("التقويم والخلاصة", "عرض المجموعات والتقويم", "تقويم · 10 دقائق", C.accent6);
    card(s, 6.6, 1.45, 6.13, 5.4, C.background2);
    txt(s, "عرض ومناقشة", { x: 6.85, y: 1.6, w: 5.63, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
    const steps = [
      "يعرض «العارض» في كل مجموعة حلّ تمرين واحد على اللوح.",
      "تتحقّق مجموعة أخرى من المستوى نفسه وتطرح سؤالًا.",
      "نقارن طرائق الحل ونصحّح الأخطاء الشائعة معًا.",
      "يربط المعلّم بين حلول المستويات الثلاثة والقاعدة.",
    ];
    steps.forEach((t, i) => {
      const y = 2.3 + i * 1.08;
      numberBadge(s, i + 1, 12.0, y + 0.08, 0.48, C.accent6);
      txt(s, t, { x: 6.85, y, w: 5.0, h: 0.9, fontSize: 16 });
    });
    // exit ticket
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.45, w: 5.7, h: 2.6, rectRadius: 0.15, fill: { color: C.text2 }, line: { type: "none" }, objectName: "exit-ticket" });
    iconCircle(s, ic.ticket, 5.35, 1.65, 0.7, C.accent2);
    txt(s, "بطاقة الخروج · دقيقتان", { x: 0.85, y: 1.7, w: 4.4, h: 0.6, fontSize: 19, bold: true, color: C.background1, valign: "middle" });
    txt(s, "حلّ في ℝ:", { x: 0.85, y: 2.45, w: 4.9, h: 0.5, fontSize: 16, color: C.background2 });
    s.addText("x² − 4 > 0", { x: 0.85, y: 2.95, w: 5.2, h: 0.85, fontSize: 30, bold: true, color: C.background1, align: "center", valign: "middle", isTextBox: true, rtlMode: false });
    // self assessment
    card(s, 0.6, 4.3, 5.7, 2.55, C.background2);
    txt(s, "تقويم ذاتي: أين أنا الآن؟", { x: 0.85, y: 4.4, w: 5.2, h: 0.5, fontSize: 17, bold: true, color: C.text2 });
    const self = [[C.accent3, "أحلّ المتراجحة وحدي"], [C.accent4, "أحتاج إلى مساعدة بسيطة"], [C.accent2, "أحتاج إلى مراجعة القاعدة"]];
    self.forEach(([col, t], i) => {
      const y = 5.0 + i * 0.6;
      s.addShape(pres.shapes.OVAL, { x: 5.55, y: y + 0.08, w: 0.38, h: 0.38, fill: { color: col }, line: { type: "none" }, objectName: "traffic-light" });
      txt(s, t, { x: 0.85, y, w: 4.55, h: 0.55, fontSize: 15, valign: "middle" });
    });
    s.addNotes("حل بطاقة الخروج: الجذران −2 و 2 ، a > 0 ⟵ S = ]−∞ ; −2[ ∪ ]2 ; +∞[.\nتُجمع البطاقات لتحديد من يحتاج إلى دعم في الحصة القادمة.");
  }

  // ===== 16. Summary =====
  {
    const s = pres.addSlide({ masterName: "CLOSING", sectionTitle: "التقويم والخلاصة" });
    s.addText("الخلاصة", { placeholder: "title", ...AR });
    const pts = [
      [ic.table, "ثلاثي الحدود يأخذ إشارة a دائمًا، إلا بين الجذرين عندما " + m("Δ > 0")],
      [ic.pen, "نرتّب ⟵ نحسب Δ والجذور ⟵ جدول الإشارة ⟵ مجموعة الحلول"],
      [ic.check, "الجذور داخلة أو مستثناة حسب الرمز:"],
    ];
    pts.forEach(([img, t], i) => {
      const y = 1.8 + i * 1.15;
      iconCircle(s, img, 11.75, y, 0.8, C.accent1);
      txt(s, t, { x: i === 2 ? 6.6 : 0.8, y: y - 0.05, w: i === 2 ? 4.9 : 10.7, h: 0.9, fontSize: 21, color: C.background1, valign: "middle" });
    });
    mathTxt(s, "≤ , ≥  →  [ ]        < , >  →  ] [", { x: 0.8, y: 4.1, w: 5.6, h: 0.8, fontSize: 21, bold: true, color: C.background1, align: "center" });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 5.4, w: 11.75, h: 1.4, rectRadius: 0.15, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "homework" });
    iconCircle(s, ic.book, 11.55, 5.7, 0.8, C.text2);
    txt(s, "واجب منزلي: حلّ في ℝ", { x: 7.0, y: 5.4, w: 4.4, h: 1.4, fontSize: 21, bold: true, color: C.background1, valign: "middle" });
    mathTxt(s, "(2)  4x² − 4x + 1 ≤ 0          (1)  −x² + x + 6 > 0", { x: 1.0, y: 5.4, w: 6.0, h: 1.4, fontSize: 22, bold: true, color: C.background1, align: "center" });
    s.addNotes("حل الواجب: (1) x² − x − 6 < 0 ⟵ S = ]−2 ; 3[. (2) (2x − 1)² ≤ 0 ⟵ S = {1/2}.");
  }

  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const fs = require("fs");
  const zip = await JSZip.loadAsync(fs.readFileSync(OUT));
  const tp = "ppt/theme/theme1.xml";
  const xml = (await zip.file(tp).async("string")).replace(/<a:cs typeface=""\/>/g, '<a:cs typeface="Arial"/>');
  zip.file(tp, xml);
  fs.writeFileSync(OUT, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
  console.log("wrote", OUT);
})();
