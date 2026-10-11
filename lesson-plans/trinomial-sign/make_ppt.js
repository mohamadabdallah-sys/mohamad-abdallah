// Lesson deck: إشارة ثلاثي الحدود من الدرجة الثانية.
// usage: python3 figs.py && NODE_PATH=<dir with pptxgenjs, react, react-dom, react-icons, sharp> node make_ppt.js [apply_theme.js]
//        then python3 animate.py (answers appear on click)
// Slide numbers follow the lesson plan: 3 = warm-up, 4 = curve of x² − x − 6, 5 = pair work, 6 = the rule.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react"), RDS = require("react-dom/server"), sharp = require("sharp");
const fa = require("react-icons/fa");

const OUT = path.join(__dirname, "عرض-إشارة-ثلاثي-الحدود.pptx");
const THEME = {
  name: "Trinomial sign", headFontFace: "Arial", bodyFontFace: "Arial",
  colors: {
    dk1: "172231", lt1: "FFFFFF", dk2: "123B4A", lt2: "EDF3F5",
    accent1: "1F6F8B", accent2: "F2A541", accent3: "2F7D46", accent4: "C2452F", accent5: "6C4AB6", accent6: "4F5C6E",
    hlink: "1F6F8B", folHlink: "6C4AB6",
  },
};
const MATH = "Cambria";
const MUTED = "5B6878";

async function icon(name, color = "#FFFFFF", px = 256) {
  const svg = RDS.renderToStaticMarkup(React.createElement(fa[name], { color, size: px }));
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
async function fig(key) {
  const buf = await sharp(fs.readFileSync(path.join(__dirname, "figs", key + ".svg")), { density: 220 }).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// "x^2 − 5x + 6" -> runs with superscripts
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

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.rtlMode = true;
  pres.title = "إشارة ثلاثي الحدود من الدرجة الثانية";
  pres.subject = "رياضيات – المتراجحات من الدرجة الثانية";
  pres.author = "Mohamad Abdallah";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const POS = C.accent3, NEG = C.accent4;
  const shadow = () => ({ type: "outer", color: "1B2A44", opacity: 0.14, blur: 8, offset: 2, angle: 90 });

  const ICON = {};
  for (const n of ["FaBullseye", "FaBookOpen", "FaSearch", "FaUserFriends", "FaLightbulb", "FaPencilAlt", "FaChartLine", "FaEye",
    "FaUsers", "FaBrain", "FaHandsHelping", "FaRocket", "FaComments", "FaHome", "FaFlagCheckered", "FaChalkboard", "FaIdCard", "FaDesktop"])
    ICON[n] = await icon(n);
  const FIG = {};
  for (const k of ["f1", "g1", "g2", "g3", "neg", "title"]) FIG[k] = await fig(k);

  // ---------- layouts ----------
  pres.defineSlideMaster({
    title: "DARK", background: { color: C.text2 },
    objects: [{ placeholder: { options: { name: "title", type: "title", x: 6.2, y: 1.6, w: 6.53, h: 2.0, fontSize: 44, bold: true,
      color: C.background1, align: "right", valign: "middle", rtlMode: true }, text: "" } }],
  });
  pres.defineSlideMaster({
    title: "CONTENT", background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 4.2, y: 0.32, w: 8.53, h: 0.85, fontSize: 32, bold: true,
        color: C.text2, align: "right", valign: "middle", rtlMode: true, margin: 0 }, text: "" } },
      { text: { text: "إشارة ثلاثي الحدود من الدرجة الثانية", options: { x: 6.73, y: 7.02, w: 6.0, h: 0.3, fontSize: 10,
        color: "7C8797", align: "right", rtlMode: true, margin: 0 } } },
    ],
    slideNumber: { x: 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: "7C8797", margin: 0 },
  });

  // ---------- helpers ----------
  const ar = (s, t, o) => s.addText(Array.isArray(t) ? t : [{ text: t, options: { rtlMode: true, lang: "ar-SA" } }],
    { isTextBox: true, rtlMode: true, lang: "ar-SA", align: "right", valign: "top", fontSize: 16, color: C.text1, margin: 0.05, ...o });
  const mt = (s, t, o) => s.addText(Array.isArray(t) ? t : runs(t), { isTextBox: true, fontFace: MATH, align: "center",
    valign: "middle", fontSize: 26, color: C.text1, margin: 0.05, ...o });
  // Arabic sentence with inline math pieces: ["احسب ", {m:"Δ"}, " للمعادلة"]
  const mix = (parts, base = {}) => parts.flatMap((p) => typeof p === "string"
    ? [{ text: p, options: { rtlMode: true, lang: "ar-SA", ...base } }]
    : runs(p.m, { fontFace: MATH, ...base, ...(p.o || {}) }));
  const card = (s, x, y, w, h, o = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: o.fill || C.background2, transparency: o.tr || 0 },
    line: { color: o.line || o.fill || C.background2, width: o.lw || 0.75, transparency: o.ltr ?? (o.tr || 0) },
    shadow: o.noShadow ? undefined : shadow(), objectName: o.name });
  const badge = (s, x, y, d, ic, color) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color } });
    if (ic) s.addImage({ data: ICON[ic], x: x + d * 0.26, y: y + d * 0.26, w: d * 0.48, h: d * 0.48 });
  };
  const num = (s, x, y, d, n, color) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color } });
    s.addText(String(n), { isTextBox: true, x, y, w: d, h: d, fontSize: d * 26, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
  };
  const chip = (s, text, color, ic) => {
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
  // objects named rv<k>_* appear on click k (animate.py)
  let rvn = 0;
  const rv = (k) => `rv${k}_${++rvn}`;
  const cover = (s, x, y, w, h, k, fill = "FFFFFF") => s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, objectName: rv(k) });

  // Sign table, x increasing left to right. xs: labels incl. ±∞; f: [interval, point, interval, ...]
  // reveal: click number for the f-row contents (blank row before the click); rowLabel: label of the 2nd row
  const signTable = (s, x, y, w, xs, f, o = {}) => {
    const lab = o.lab ?? 1.25, rh = o.rh ?? 0.62, fs = o.fs ?? 20;
    const bw = w - lab, n = xs.length, step = bw / (n - 1), pad = o.pad ?? 0.45;
    const px = (i) => x + lab + pad + i * ((bw - 2 * pad) / (n - 1));
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: rh * 2, fill: { color: "FFFFFF" }, line: { color: "9AA5B4", width: 1.25 } });
    s.addShape(pres.shapes.LINE, { x, y: y + rh, w, h: 0, line: { color: "9AA5B4", width: 1.25 } });
    s.addShape(pres.shapes.LINE, { x: x + lab, y, w: 0, h: rh * 2, line: { color: "9AA5B4", width: 1.25 } });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.01, y: y + 0.01, w: lab - 0.02, h: rh * 2 - 0.02, fill: { color: C.background2 }, line: { color: C.background2 } });
    mt(s, runs("x", { italic: true }), { x, y, w: lab, h: rh, fontSize: fs });
    mt(s, runs(o.label || "f(x)", { italic: true }), { x, y: y + rh, w: lab, h: rh, fontSize: fs - 2 });
    xs.forEach((t, i) => mt(s, t, { x: px(i) - 0.6, y, w: 1.2, h: rh, fontSize: fs, bold: true, color: C.text2 }));
    const items = [];
    f.forEach((v, j) => {
      const isPoint = j % 2 === 1, i = Math.floor(j / 2);
      const cx = isPoint ? px(i + 1) : (px(i) + px(i + 1)) / 2;
      items.push([cx, v, isPoint]);
    });
    const k = o.reveal;
    items.forEach(([cx, v, isPoint]) => {
      if (isPoint) s.addShape(pres.shapes.LINE, { x: cx, y: y + rh, w: 0, h: rh, line: { color: "C9D2DE", width: 1, dashType: "dash" } });
    });
    items.forEach(([cx, v, isPoint]) => {
      if (v === "") return;
      const col = v === "+" ? POS : v === "−" ? NEG : C.text1;
      const isText = /[؀-ۿ]/.test(v);
      const bw2 = isText ? Math.min(2.6, step * 1.0) : (isPoint ? 0.42 : 0.9);
      const opt = { x: cx - bw2 / 2, y: y + rh + 0.06, w: bw2, h: rh - 0.12, fontSize: isText ? fs - 3 : fs + 4, bold: true, color: col,
        objectName: k ? rv(k) : undefined, fill: isPoint ? { color: "FFFFFF" } : undefined };
      if (isText) ar(s, v, { ...opt, align: "center", valign: "middle", color: v.includes("عكس") ? NEG : POS, margin: 0 });
      else mt(s, v, { ...opt, margin: 0 });
    });
  };

  // =====================================================================
  // 1. Title
  pres.addSection({ title: "البداية" });
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "البداية" });
    s.addText("إشارة ثلاثي الحدود من الدرجة الثانية", { placeholder: "title", rtlMode: true, lang: "ar-SA" });
    mt(s, runs("f(x) = ax^2 + bx + c", { italic: true, color: C.accent2, bold: true }), { x: 6.2, y: 3.75, w: 6.53, h: 0.8, fontSize: 32, align: "right" });
    ar(s, "المتراجحات من الدرجة الثانية · مدّة الحصّة 45 دقيقة + التقييم", { x: 6.2, y: 4.65, w: 6.53, h: 0.5, fontSize: 18, color: C.background2 });
    card(s, 0.8, 1.1, 5.0, 4.06, { fill: "FFFFFF", noShadow: true });
    s.addImage({ data: FIG.title, x: 0.95, y: 1.22, w: 4.7, h: 3.82 });
    [["فوق المحور: f(x) > 0", POS], ["تحت المحور: f(x) < 0", NEG]].forEach(([t, col], k) => {
      const x = 0.8 + k * 2.55;
      card(s, x, 5.45, 2.45, 0.6, { fill: col, noShadow: true });
      ar(s, t, { x, y: 5.45, w: 2.45, h: 0.6, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle" });
    });
    s.addNotes("نعرض عنوان الحصّة. المنحنى الأخضر فوق محور الفواصل والأحمر تحته: هذه هي فكرة الحصّة كلّها، وسنعود إليها في الشريحة 4.");
  }

  // 2. Goals, terms, learning styles
  {
    const s = content("البداية", "أهداف الحصّة والمصطلحات",
      "نقرأ الهدفين. نشير إلى المصطلحات الجديدة: متراجحة من الدرجة الثانية، ثلاثي الحدود، المميّز Δ، الجذر، جدول الإشارة. أنماط التعلّم: رياضي-منطقي (حساب Δ والقاعدة)، مكاني-بصري (قراءة المنحنى)، اجتماعي (العمل الثنائي).");
    ar(s, "في نهاية الحصّة يتوقّع أن يصبح التلميذ قادرًا على أن:", { x: 4.6, y: 1.35, w: 8.13, h: 0.45, fontSize: 16, color: MUTED });
    const goals = [
      mix(["يربط إشارة ثلاثي الحدود ", { m: "f(x) = ax^2 + bx + c" }, " بموقع منحنيه بالنسبة لمحور الفواصل."]),
      mix(["يحدّد إشارة ثلاثي الحدود حسب إشارة المميّز ", { m: "Δ" }, " وإشارة ", { m: "a" }, "."]),
    ];
    goals.forEach((g, k) => {
      const y = 1.9 + k * 1.15;
      card(s, 4.6, y, 8.13, 0.98, { fill: C.background2, noShadow: true });
      num(s, 12.0, y + 0.24, 0.5, k + 1, C.accent1);
      ar(s, g, { x: 4.75, y, w: 7.1, h: 0.98, fontSize: 17, valign: "middle" });
    });
    ar(s, "المصطلحات", { x: 4.6, y: 4.3, w: 8.13, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
    const terms = [["متراجحة من الدرجة الثانية", null], ["ثلاثي الحدود", "ax^2 + bx + c"], ["المميّز", "Δ = b^2 − 4ac"], ["جذر", "f(x_0) = 0"], ["جدول الإشارة", null]];
    const tw = [2.9, 2.35, 2.35], rowsT = [[0, 1, 2], [3, 4]];
    rowsT.forEach((row, r) => {
      let xr = 12.73;
      row.forEach((k) => {
        const w = r === 0 ? tw[row.indexOf(k)] : 2.6;
        const [t, m] = terms[k];
        const x = xr - w;
        card(s, x, 4.9 + r * 0.98, w, 0.82, { fill: C.background1, line: "DCE2E9", noShadow: true });
        if (m) {
          ar(s, t, { x: x + 0.1, y: 4.92 + r * 0.98, w: w - 0.2, h: 0.4, fontSize: 15, bold: true, color: C.text2, align: "center" });
          mt(s, m.replace("x_0", "x₀"), { x: x + 0.1, y: 5.3 + r * 0.98, w: w - 0.2, h: 0.4, fontSize: 15, color: C.accent1 });
        } else ar(s, t, { x: x + 0.1, y: 4.9 + r * 0.98, w: w - 0.2, h: 0.82, fontSize: 15, bold: true, color: C.text2, align: "center", valign: "middle" });
        xr = x - 0.18;
      });
    });
    card(s, 0.6, 1.35, 3.6, 5.37, { fill: C.text2, noShadow: true });
    ar(s, "أنماط التعلّم", { x: 0.8, y: 1.5, w: 3.2, h: 0.5, fontSize: 20, bold: true, color: C.accent2, align: "center" });
    [["رياضي – منطقي", "FaBrain"], ["مكاني – بصري", "FaEye"], ["اجتماعي", "FaUserFriends"]].forEach(([t, ic], k) => {
      const y = 2.15 + k * 1.5;
      badge(s, 1.95, y, 0.9, ic, C.accent1);
      ar(s, t, { x: 0.8, y: y + 0.92, w: 3.2, h: 0.45, fontSize: 17, bold: true, color: C.background1, align: "center" });
    });
  }

  // 3. Warm-up (slide 3 in the plan)
  pres.addSection({ title: "التمهيد" });
  {
    const s = content("التمهيد", "تمهيد: نتذكّر",
      "التمهيد (10 د) – ربط بالمكتسبات السابقة. يحلّ التلاميذ الأسئلة الثلاثة فرديًّا (بطاقة التمهيد). ثم تصحيح جماعي سريع: كل نقرة تُظهر إجابة سؤال. نسجّل من أخطأ في كل سؤال لتوزيع التلاميذ على الفئات في الحصّة الثانية.\nالإجابات: (1) Δ = 1، الحلّان 2 و3. (2) Δ = −23 < 0 لا حلول. (3) 2x − 4 سالب قبل 2، صفر عند 2، موجب بعد 2.");
    chip(s, "التمهيد · 10 د", C.accent1, "FaPencilAlt");
    ar(s, "حلّ فرديًّا:", { x: 8.73, y: 1.3, w: 4.0, h: 0.45, fontSize: 18, color: MUTED });
    const Q = [
      ["حلّ المعادلة", "x^2 − 5x + 6 = 0"],
      ["احسب المميّز Δ للمعادلة", "2x^2 + x + 3 = 0"],
      ["أكمل جدول إشارة", "2x − 4"],
    ];
    Q.forEach(([t, m], k) => {
      const x = 12.73 - (k + 1) * 3.93 - k * 0.17;
      card(s, x, 1.85, 3.93, 4.9, { fill: C.background1, line: "DCE2E9" });
      num(s, x + 3.3, 2.0, 0.5, k + 1, C.accent1);
      ar(s, t, { x: x + 0.15, y: 2.0, w: 3.1, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
      mt(s, runs(m, { bold: true }), { x: x + 0.1, y: 2.6, w: 3.73, h: 0.75, fontSize: 25, color: C.accent1 });
      s.addShape(pres.shapes.LINE, { x: x + 0.4, y: 3.55, w: 3.13, h: 0, line: { color: "DCE2E9", width: 1 } });
    });
    // answers
    const x1 = 12.73 - 3.93, x2 = 12.73 - 2 * 3.93 - 0.17, x3 = 12.73 - 3 * 3.93 - 0.34;
    mt(s, runs("Δ = 25 − 24 = 1"), { x: x1 + 0.1, y: 3.75, w: 3.73, h: 0.6, fontSize: 22, objectName: rv(1) });
    mt(s, runs("x = (5 − 1)/2 = 2"), { x: x1 + 0.1, y: 4.4, w: 3.73, h: 0.6, fontSize: 22, objectName: rv(1) });
    mt(s, runs("x = (5 + 1)/2 = 3"), { x: x1 + 0.1, y: 5.0, w: 3.73, h: 0.6, fontSize: 22, objectName: rv(1) });
    ar(s, "حلّان: 2 و 3", { x: x1 + 0.1, y: 5.75, w: 3.73, h: 0.6, fontSize: 20, bold: true, color: POS, align: "center", objectName: rv(1) });
    mt(s, runs("Δ = 1^2 − 4 × 2 × 3"), { x: x2 + 0.1, y: 3.75, w: 3.73, h: 0.6, fontSize: 22, objectName: rv(2) });
    mt(s, runs("Δ = 1 − 24 = −23"), { x: x2 + 0.1, y: 4.4, w: 3.73, h: 0.6, fontSize: 22, objectName: rv(2) });
    mt(s, runs("Δ < 0", { bold: true }), { x: x2 + 0.1, y: 5.05, w: 3.73, h: 0.55, fontSize: 22, color: NEG, objectName: rv(2) });
    ar(s, "لا حلول للمعادلة", { x: x2 + 0.1, y: 5.65, w: 3.73, h: 0.55, fontSize: 20, bold: true, color: NEG, align: "center", objectName: rv(2) });
    ar(s, mix(["تنعدم عند ", { m: "x = 2" }]), { x: x3 + 0.1, y: 3.75, w: 3.73, h: 0.55, fontSize: 18, align: "center", objectName: rv(3) });
    signTable(s, x3 + 0.18, 4.45, 3.57, ["−∞", "2", "+∞"], ["−", "0", "+"], { lab: 1.05, fs: 16, rh: 0.6, pad: 0.3, label: "2x−4", reveal: 3 });
  }

  // 4. Exploration – curve of x² − x − 6 (slide 4 in the plan)
  pres.addSection({ title: "الاستكشاف" });
  {
    const s = content("الاستكشاف", "المنحنى ومحور الفواصل",
      "الاستكشاف (10 د) – استقصاء موجّه على اللوح التفاعلي (يمكن فتح المنحنى نفسه في GeoGebra وتحريك نقطة عليه). نطرح الأسئلة الثلاثة واحدًا واحدًا، وكل نقرة تُظهر الإجابة. الاستنتاج: f(x) < 0 بين الجذرين −2 و3، وf(x) > 0 خارجهما. النقرة الرابعة تُظهر جدول الإشارة.");
    chip(s, "الاستكشاف · 10 د", C.accent1, "FaSearch");
    card(s, 0.6, 1.35, 6.2, 5.45, { fill: "FFFFFF", line: "DCE2E9" });
    s.addImage({ data: FIG.f1, x: 0.7, y: 1.45, w: 6.0, h: 4.5 });
    mt(s, runs("f(x) = x^2 − x − 6", { bold: true, italic: true }), { x: 0.7, y: 6.0, w: 6.0, h: 0.7, fontSize: 26, color: C.text2 });
    const Q = [
      ["أين يقطع المنحنى محور الفواصل؟", "x = −2   ;   x = 3", C.accent1],
      ["متى يقع المنحنى فوق المحور؟", "x < −2   or   x > 3   ⇒   f(x) > 0", POS],
      ["متى يقع المنحنى تحت المحور؟", "−2 < x < 3   ⇒   f(x) < 0", NEG],
    ];
    Q.forEach(([q, a, col], k) => {
      const y = 1.35 + k * 1.3;
      num(s, 12.23, y + 0.05, 0.5, k + 1, C.accent1);
      ar(s, q, { x: 7.1, y, w: 5.03, h: 0.55, fontSize: 19, bold: true, color: C.text2 });
      card(s, 7.1, y + 0.6, 5.63, 0.6, { fill: col, tr: 88, line: col, ltr: 50, noShadow: true, name: rv(k + 1) });
      mt(s, a.split("or").flatMap((p, i) => (i ? [{ text: "أو", options: { fontFace: "Arial", bold: true, color: col } }, ...runs(p, { bold: true, color: col })] : runs(p, { bold: true, color: col }))),
        { x: 7.2, y: y + 0.6, w: 5.43, h: 0.6, fontSize: 20, objectName: rv(k + 1) });
    });
    ar(s, "جدول الإشارة", { x: 7.1, y: 5.3, w: 5.63, h: 0.4, fontSize: 16, bold: true, color: C.text2, objectName: rv(4) });
    signTable(s, 7.1, 5.72, 5.63, ["−∞", "−2", "3", "+∞"], ["+", "0", "−", "0", "+"], { rh: 0.52, fs: 18, lab: 1.1, reveal: 4 });
  }

  // 5. Pair work (slide 5 in the plan)
  {
    const s = content("الاستكشاف", "عمل ثنائي: ثلاث دوال",
      "عمل ثنائي (12 د) – كل ثنائي يدرس الدوال الثلاث على بطاقة الاستكشاف: يحسب Δ، يحدّد عدد نقاط التقاطع مع محور الفواصل، ويصف إشارة الدالة. بعد العمل، كل نقرة تُظهر منحنى دالة ونتائجها للتصحيح. المتعثّرون يستعملون جدول القيم الجاهز على بطاقة الدعم.");
    chip(s, "عمل ثنائي · 12 د", C.accent5, "FaUserFriends");
    const F = [
      ["x^2 − 2x − 3", "g1", "Δ = 4 + 12 = 16 > 0", "نقطتان: −1 و 3", "سالبة بين −1 و 3، موجبة خارجهما"],
      ["x^2 − 2x + 1", "g2", "Δ = 4 − 4 = 0", "نقطة واحدة: 1", "موجبة، صفر عند 1"],
      ["x^2 − 2x + 3", "g3", "Δ = 4 − 12 = −8 < 0", "لا تقاطع", "موجبة دائمًا"],
    ];
    F.forEach(([f, g, d, n, sign], k) => {
      const x = 12.73 - (k + 1) * 3.93 - k * 0.17, k1 = k + 1;
      card(s, x, 1.35, 3.93, 5.45, { fill: C.background1, line: "DCE2E9" });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.35, w: 3.93, h: 0.75, rectRadius: 0.12, fill: { color: C.accent5 }, line: { color: C.accent5 } });
      mt(s, runs(f, { bold: true, italic: true, color: C.background1 }), { x, y: 1.35, w: 3.93, h: 0.75, fontSize: 24 });
      // placeholders
      s.addShape(pres.shapes.RECTANGLE, { x: x + 0.3, y: 2.25, w: 3.33, h: 2.5, fill: { color: C.background2 }, line: { color: "DCE2E9", dashType: "dash" } });
      ar(s, "؟", { x: x + 0.3, y: 2.25, w: 3.33, h: 2.5, fontSize: 48, color: "9AA5B4", align: "center", valign: "middle" });
      [["المميّز", 4.9], ["التقاطع", 5.5], ["الإشارة", 6.1]].forEach(([lab, y]) =>
        ar(s, lab + ":", { x: x + 2.65, y, w: 1.15, h: 0.55, fontSize: 14, bold: true, color: MUTED, valign: "middle" }));
      // reveal
      s.addImage({ data: FIG[g], x: x + 0.3, y: 2.25, w: 3.33, h: 2.5, objectName: rv(k1) });
      mt(s, runs(d, { bold: true }), { x: x + 0.1, y: 4.9, w: 2.55, h: 0.55, fontSize: 16, color: C.accent1, objectName: rv(k1) });
      ar(s, n, { x: x + 0.1, y: 5.5, w: 2.55, h: 0.55, fontSize: 15, bold: true, color: C.text2, valign: "middle", objectName: rv(k1) });
      ar(s, sign, { x: x + 0.1, y: 6.1, w: 2.55, h: 0.6, fontSize: 14, bold: true, color: k ? POS : C.text2, valign: "middle", objectName: rv(k1) });
    });
  }

  // 6. The rule (slide 6 in the plan)
  pres.addSection({ title: "التفسير" });
  {
    const s = content("التفسير", "القاعدة: إشارة ثلاثي الحدود",
      "التفسير (13 د) – تعرض الثنائيات نتائجها، ونقود صياغة القاعدة: ثلاثي الحدود يأخذ إشارة a دائمًا، إلا بين الجذرين عندما Δ > 0. يدوّن التلاميذ جداول الإشارة للحالات الثلاث في دفاترهم (x₁ و x₂ الجذران، x₀ = −b/2a الجذر المضاعف).");
    chip(s, "التفسير · 13 د", C.accent2, "FaBookOpen");
    card(s, 0.6, 1.35, 12.13, 1.0, { fill: C.text2, noShadow: true });
    ar(s, mix(["ثلاثي الحدود يأخذ ", "إشارة ", { m: "a" }, " دائمًا، إلا بين الجذرين عندما ", { m: "Δ > 0" }], { color: C.background1 }),
      { x: 0.8, y: 1.35, w: 11.73, h: 1.0, fontSize: 24, bold: true, align: "center", valign: "middle" });
    const cases = [
      ["Δ > 0", "جذران x₁ < x₂", ["−∞", "x₁", "x₂", "+∞"], ["إشارة a", "0", "عكس إشارة a", "0", "إشارة a"], C.accent1],
      ["Δ = 0", "جذر مضاعف x₀ = −b/2a", ["−∞", "x₀", "+∞"], ["إشارة a", "0", "إشارة a"], C.accent5],
      ["Δ < 0", "لا جذور", ["−∞", "+∞"], ["إشارة a"], C.accent6],
    ];
    cases.forEach(([d, sub, xs, f, col], k) => {
      const y = 2.6 + k * 1.42;
      card(s, 0.6, y, 12.13, 1.27, { fill: C.background2, noShadow: true });
      card(s, 10.7, y + 0.14, 1.88, 0.99, { fill: col, noShadow: true });
      mt(s, runs(d, { bold: true, color: C.background1 }), { x: 10.7, y: y + 0.14, w: 1.88, h: 0.99, fontSize: 26 });
      ar(s, sub, { x: 7.7, y: y + 0.14, w: 2.85, h: 0.99, fontSize: 16, bold: true, color: C.text2, valign: "middle" });
      signTable(s, 0.8, y + 0.14, 6.7, xs, f, { rh: 0.5, fs: 16, lab: 0.95 });
    });
  }

  // 7. Sign tables of the three functions
  {
    const s = content("التفسير", "جداول الإشارة في الدفتر",
      "نطبّق القاعدة على دوال الشريحة 5 (a = 1 > 0 في الثلاث). يدوّن التلاميذ الجداول في دفاترهم. نؤكّد: عند Δ = 0 الدالة لا تتغيّر إشارتها، لكنها تنعدم عند الجذر.");
    chip(s, "التفسير · 13 د", C.accent2, "FaBookOpen");
    const rows = [
      ["x^2 − 2x − 3", "Δ = 16 > 0", ["−∞", "−1", "3", "+∞"], ["+", "0", "−", "0", "+"], "g1"],
      ["x^2 − 2x + 1", "Δ = 0", ["−∞", "1", "+∞"], ["+", "0", "+"], "g2"],
      ["x^2 − 2x + 3", "Δ = −8 < 0", ["−∞", "+∞"], ["+"], "g3"],
    ];
    rows.forEach(([f, d, xs, sg, g], k) => {
      const y = 1.35 + k * 1.83;
      card(s, 0.6, y, 12.13, 1.65, { fill: C.background1, line: "DCE2E9" });
      mt(s, runs(f, { bold: true, italic: true }), { x: 9.6, y: y + 0.2, w: 3.0, h: 0.7, fontSize: 24, color: C.text2, align: "right" });
      mt(s, runs(d), { x: 9.6, y: y + 0.85, w: 3.0, h: 0.55, fontSize: 18, color: C.accent1, align: "right" });
      signTable(s, 3.0, y + 0.3, 6.3, xs, sg, { rh: 0.52, fs: 18, lab: 1.0 });
      s.addImage({ data: FIG[g], x: 0.75, y: y + 0.12, w: 1.88, h: 1.41 });
    });
  }

  // 8. Differentiation
  pres.addSection({ title: "الفروقات الفردية" });
  {
    const s = content("الفروقات الفردية", "لكلٍّ حسب حاجته",
      "للمتعثّرين: جدول قيم جاهز للدالة x² − x − 6 لقراءة المنحنى (القيم 0 تعني الجذور، القيم الموجبة فوق المحور). للمتفوّقين: ماذا يتغيّر إذا كان a < 0؟ النقرة تُظهر منحنى −x² + x + 6 والاستنتاج: تنقلب الإشارات، فتكون الدالة موجبة بين الجذرين وسالبة خارجهما — أي تبقى القاعدة نفسها: إشارة a خارج الجذرين.");
    chip(s, "الفروقات الفرديّة", C.accent3, "FaHandsHelping");
    // support: table of values
    card(s, 6.83, 1.35, 5.9, 5.45, { fill: C.accent3, tr: 90, line: C.accent3, ltr: 50 });
    badge(s, 11.75, 1.55, 0.75, "FaHandsHelping", C.accent3);
    ar(s, "دعم: جدول قيم جاهز", { x: 7.0, y: 1.6, w: 4.6, h: 0.6, fontSize: 22, bold: true, color: C.accent3 });
    mt(s, runs("f(x) = x^2 − x − 6", { italic: true, bold: true }), { x: 7.0, y: 2.25, w: 5.55, h: 0.55, fontSize: 20, color: C.text2 });
    const xsV = [-3, -2, -1, 0, 1, 2, 3, 4];
    const fv = xsV.map((x) => x * x - x - 6);
    const cell = (t, o = {}) => ({ text: String(t).replace("-", "−"), options: { align: "center", fontFace: MATH, ...o } });
    s.addTable([
      [cell("x", { bold: true, italic: true, fill: { color: C.background2 } }), ...xsV.map((x) => cell(x, { bold: true, fill: { color: C.background2 } }))],
      [cell("f(x)", { bold: true, italic: true, fill: { color: C.background2 } }), ...fv.map((v) => cell(v, { bold: true, color: v > 0 ? "2F7D46" : v < 0 ? "C2452F" : "172231", fill: { color: "FFFFFF" } }))],
    ], { x: 7.0, y: 3.0, w: 5.55, colW: [0.83, ...Array(8).fill(0.59)], rowH: [0.55, 0.55], fontSize: 16, valign: "middle", border: { type: "solid", pt: 1, color: "C9D2DE" }, color: C.text1 });
    ar(s, mix([{ m: "f(x) = 0" }, " ← جذر: المنحنى يقطع المحور"]), { x: 7.0, y: 4.35, w: 5.55, h: 0.5, fontSize: 16 });
    ar(s, mix([{ m: "f(x) > 0", o: { color: "2F7D46" } }, " ← المنحنى فوق المحور"]), { x: 7.0, y: 4.9, w: 5.55, h: 0.5, fontSize: 16 });
    ar(s, mix([{ m: "f(x) < 0", o: { color: "C2452F" } }, " ← المنحنى تحت المحور"]), { x: 7.0, y: 5.45, w: 5.55, h: 0.5, fontSize: 16 });
    // enrichment
    card(s, 0.6, 1.35, 5.9, 5.45, { fill: C.text2 });
    badge(s, 5.5, 1.55, 0.75, "FaRocket", C.accent2);
    ar(s, mix(["إثراء: ماذا يتغيّر إذا كان ", { m: "a < 0" }, "؟"]), { x: 0.8, y: 1.6, w: 4.6, h: 0.6, fontSize: 21, bold: true, color: C.accent2 });
    mt(s, runs("f(x) = −x^2 + x + 6", { italic: true, bold: true, color: C.background1 }), { x: 0.8, y: 2.25, w: 5.5, h: 0.55, fontSize: 20 });
    ar(s, "ارسم أو تخيّل المنحنى، ثم قارن مع x² − x − 6", { x: 0.8, y: 2.85, w: 5.5, h: 0.5, fontSize: 15, color: C.background2, align: "center" });
    card(s, 0.85, 3.4, 5.4, 2.35, { fill: "FFFFFF", noShadow: true, name: rv(1) });
    s.addImage({ data: FIG.neg, x: 2.0, y: 3.45, w: 3.0, h: 2.25, objectName: rv(1) });
    ar(s, "تنقلب الإشارات: موجبة بين الجذرين وسالبة خارجهما", { x: 0.8, y: 5.85, w: 5.5, h: 0.45, fontSize: 15, bold: true, color: C.accent2, align: "center", objectName: rv(1) });
    ar(s, mix(["القاعدة نفسها: إشارة ", { m: "a" }, " خارج الجذرين"]), { x: 0.8, y: 6.27, w: 5.5, h: 0.45, fontSize: 15, color: C.background1, align: "center", objectName: rv(1) });
  }

  // 9. Oral assessment
  pres.addSection({ title: "التقييم" });
  {
    const s = content("التقييم", "تقييم شفهي: من دون رسم",
      "أسئلة شفهيّة: يحدّد التلاميذ الإشارة من دون رسم، فقط من Δ وإشارة a. النقرة الأولى تُظهر حلّ الدالة الأولى، والثانية حلّ الثانية.\n(1) Δ = 16 − 12 = 4 > 0، الجذران 1 و3، a = 1 > 0: موجبة خارج [1 ; 3] وسالبة بينهما.\n(2) Δ = 4 − 20 = −16 < 0، a = −1 < 0: سالبة دائمًا.");
    chip(s, "أسئلة شفهيّة", C.accent4, "FaComments");
    const F = [
      ["x^2 − 4x + 3", "Δ = 16 − 12 = 4 > 0", "الجذران 1 و 3 ، a = 1 > 0", ["−∞", "1", "3", "+∞"], ["+", "0", "−", "0", "+"]],
      ["−x^2 + 2x − 5", "Δ = 4 − 20 = −16 < 0", "لا جذور ، a = −1 < 0", ["−∞", "+∞"], ["−"]],
    ];
    F.forEach(([f, d, r, xs, sg], k) => {
      const x = 12.73 - (k + 1) * 5.9 - k * 0.33, k1 = k + 1;
      card(s, x, 1.35, 5.9, 5.45, { fill: C.background1, line: "DCE2E9" });
      num(s, x + 5.2, 1.55, 0.5, k1, C.accent4);
      mt(s, runs("f(x) = " + f, { bold: true, italic: true }), { x: x + 0.2, y: 1.5, w: 4.9, h: 0.8, fontSize: 28, color: C.text2 });
      ar(s, "ما إشارة f(x)؟", { x: x + 0.2, y: 2.35, w: 5.5, h: 0.5, fontSize: 18, color: MUTED, align: "center" });
      mt(s, runs(d, { bold: true }), { x: x + 0.2, y: 3.0, w: 5.5, h: 0.6, fontSize: 22, color: C.accent1, objectName: rv(k1) });
      ar(s, mix(r.split(" ، ").flatMap((p, i) => (i ? ["  ،  ", { m: p }] : [p]))), { x: x + 0.2, y: 3.65, w: 5.5, h: 0.55, fontSize: 18, align: "center", objectName: rv(k1) });
      signTable(s, x + 0.35, 4.45, 5.2, xs, sg, { rh: 0.55, fs: 18, lab: 1.0, reveal: k1 });
      ar(s, k ? "سالبة دائمًا" : "سالبة بين 1 و 3، موجبة خارجهما", { x: x + 0.2, y: 5.8, w: 5.5, h: 0.6, fontSize: 18, bold: true, color: k ? NEG : C.text2, align: "center", objectName: rv(k1) });
    });
  }

  // 10. Homework
  pres.addSection({ title: "الختام" });
  {
    const s = content("الختام", "الواجب البيتي",
      "الواجب: دراسة إشارة 2x² − 3x − 2 (Δ = 25، الجذران −1/2 و 2) و x² + 6x + 9 (Δ = 0، الجذر −3). بطاقة الدعم: جدول إشارة جاهز للتعبئة للدالة x² − 9.");
    chip(s, "الواجب البيتي", C.accent1, "FaHome");
    ar(s, "ادرس إشارة كلٍّ من:", { x: 6.0, y: 1.4, w: 6.73, h: 0.55, fontSize: 22, bold: true, color: C.text2 });
    ["2x^2 − 3x − 2", "x^2 + 6x + 9"].forEach((f, k) => {
      const x = 12.73 - (k + 1) * 5.9 - k * 0.33;
      card(s, x, 2.1, 5.9, 1.4, { fill: C.background2, noShadow: true });
      num(s, x + 5.2, 2.55, 0.5, k + 1, C.accent1);
      mt(s, runs(f, { bold: true, italic: true }), { x: x + 0.2, y: 2.1, w: 4.9, h: 1.4, fontSize: 32, color: C.text2 });
    });
    ar(s, "خطوات: احسب Δ ← حدّد الجذور ← انظر إلى إشارة a ← ارسم جدول الإشارة", { x: 0.6, y: 3.7, w: 12.13, h: 0.5, fontSize: 17, color: MUTED, align: "center" });
    card(s, 0.6, 4.45, 12.13, 2.3, { fill: C.accent3, tr: 90, line: C.accent3, ltr: 50, noShadow: true });
    badge(s, 11.85, 4.65, 0.7, "FaIdCard", C.accent3);
    ar(s, mix(["بطاقة دعم: أكمل جدول إشارة ", { m: "x^2 − 9" }]), { x: 6.5, y: 4.7, w: 5.2, h: 0.55, fontSize: 19, bold: true, color: C.accent3 });
    ar(s, mix(["تلميح: ", { m: "x^2 − 9 = 0" }, " عندما ", { m: "x = −3" }, " أو ", { m: "x = 3" }]), { x: 6.5, y: 5.35, w: 5.2, h: 0.5, fontSize: 16 });
    signTable(s, 0.85, 4.95, 5.4, ["−∞", "−3", "3", "+∞"], ["", "", "", "", ""], { rh: 0.6, fs: 18, lab: 1.1, label: "x^2−9" });
  }

  // 11. Closing
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "الختام" });
    ar(s, "خلاصة الحصّة", { x: 2.0, y: 0.55, w: 10.53, h: 0.9, fontSize: 40, bold: true, color: C.background1, valign: "middle" });
    s.addImage({ data: ICON.FaFlagCheckered, x: 0.8, y: 0.7, w: 0.6, h: 0.6 });
    const K = [
      [mix(["المنحنى فوق محور الفواصل: ", { m: "f(x)" }, " موجبة؛ وتحته: سالبة"]), C.accent2],
      [mix([{ m: "Δ > 0" }, ": إشارة ", { m: "a" }, " خارج الجذرين، وعكسها بينهما"]), C.accent2],
      [mix([{ m: "Δ = 0" }, ": إشارة ", { m: "a" }, "، وتنعدم عند الجذر المضاعف"]), C.accent2],
      [mix([{ m: "Δ < 0" }, ": إشارة ", { m: "a" }, " دائمًا"]), C.accent2],
    ];
    K.forEach(([t], k) => {
      const y = 1.75 + k * 1.2;
      card(s, 0.8, y, 11.73, 1.0, { fill: C.accent1, noShadow: true });
      num(s, 11.85, y + 0.22, 0.56, k + 1, C.accent2);
      ar(s, t, { x: 1.0, y, w: 10.7, h: 1.0, fontSize: 22, bold: true, color: C.background1, valign: "middle" });
    });
    s.addNotes("نعود إلى الهدفين: هل يستطيع كل تلميذ ربط الإشارة بموقع المنحنى، وتحديدها من Δ وإشارة a؟ (الفقرة التأمّليّة: تحقّق الأهداف).");
  }

  await pres.writeFile({ fileName: OUT });
  const applyThemePath = process.argv[2];
  if (applyThemePath) await require(applyThemePath).applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
