const pptxgen = require("pptxgenjs");
const React = require("react");
const RDS = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";

const THEME = {
  name: "Force Quest",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1B2A49", lt1: "FFFFFF", dk2: "33415C", lt2: "EEF3FA",
    accent1: "13A89E", // explore - teal
    accent2: "F26B1D", // apply - orange
    accent3: "6C4AB6", // assess - purple
    accent4: "FFC93C", // gold
    accent5: "E63946", // red
    accent6: "2E86DE", // blue
    hlink: "2E86DE", folHlink: "6C4AB6",
  },
};
const H = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.rtlMode = true;
pres.title = "مغامرة القوى - لعبة استكشافية";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333;
const AR = { rtlMode: true, lang: "ar-SA" };

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.2, w: 11.9, h: 1.5, fontSize: 54, bold: true, color: C.background1, align: "center", valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 1.2, y: 3.8, w: 10.9, h: 0.9, fontSize: 24, color: C.accent4, align: "center", valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SECTION",
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 3.6, w: 11.9, h: 1.2, fontSize: 48, bold: true, color: C.background1, align: "center", valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 1.2, y: 4.8, w: 10.9, h: 1.0, fontSize: 22, color: C.background2, align: "center", valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 3.2, y: 0.35, w: 9.5, h: 0.9, fontSize: 36, bold: true, color: C.text1, align: "right", valign: "middle" }, text: "" } },
  ],
  slideNumber: { x: 0.4, y: 6.95, w: 0.6, h: 0.35, fontSize: 11, color: C.text2 },
});

// ---------- helpers ----------
async function icon(Comp, color, size = 256) {
  const svg = RDS.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
let objN = 0;
const name = (p) => `${p}-${++objN}`;

function txt(slide, text, o) {
  slide.addText(text, { isTextBox: true, align: "right", valign: "top", fontSize: 16, color: C.text1, ...AR, objectName: name("text"), ...o });
}
function card(slide, x, y, w, h, fill, o = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.15, fill: { color: fill }, line: { color: fill },
    shadow: { type: "outer", color: "1B2A49", opacity: 0.18, blur: 6, offset: 2, angle: 90 },
    objectName: name("card"), ...o,
  });
}
async function badge(slide, x, y, d, bg, Comp, fg = "FFFFFF") {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: bg }, line: { color: bg }, objectName: name("badge") });
  const p = d * 0.22;
  slide.addImage({ data: await icon(Comp, fg), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: name("icon") });
}
// station chip at top-left of content slides: the game motif
async function chip(slide, label, colorKey, hex, Comp) {
  card(slide, 0.6, 0.5, 2.3, 0.6, colorKey, { shadow: undefined, rectRadius: 0.3 });
  slide.addImage({ data: await icon(Comp, "FFFFFF"), x: 2.4, y: 0.6, w: 0.4, h: 0.4, objectName: name("icon") });
  txt(slide, label, { x: 0.7, y: 0.5, w: 1.65, h: 0.6, fontSize: 15, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
}
function title(slide, t) { slide.addText(t, { placeholder: "title", ...AR }); }

(async () => {
  // ================= 1. Title =================
  pres.addSection({ title: "البداية" });
  let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "البداية" });
  await badge(s, 5.92, 0.6, 1.5, C.accent4, fa.FaRocket, H.dk1);
  title(s, "مغامرة القوى");
  s.addText("لعبة استكشافية: استكشف · طبّق · قيّم", { placeholder: "body", ...AR });
  const st = [["استكشاف", C.accent1, fa.FaSearch], ["تطبيق", C.accent2, fa.FaTools], ["تقييم", C.accent3, fa.FaTrophy]];
  for (let i = 0; i < 3; i++) {
    const x = 8.6 - i * 3.3;
    card(s, x, 5.25, 2.9, 0.9, st[i][1], { shadow: undefined, rectRadius: 0.45 });
    s.addImage({ data: await icon(st[i][2], "FFFFFF"), x: x + 2.15, y: 5.45, w: 0.5, h: 0.5, objectName: name("icon") });
    txt(s, `المحطة ${i + 1}: ${st[i][0]}`, { x: x + 0.15, y: 5.25, w: 2.0, h: 0.9, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
  }
  s.addNotes("افتتاح اللعبة: يُقسَّم الصف إلى فرق من 4 طلاب. كل فريق يمثل طاقم مستكشفين في مهمة لاكتشاف أسرار القوى عبر ثلاث محطات.");

  // ================= 2. Rules =================
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "البداية" });
  title(s, "قواعد اللعبة");
  const rules = [
    [fa.FaUsers, C.accent6, "فرق المستكشفين", "4 طلاب في كل فريق: قائد، مُسجِّل، مُجرِّب، مُتحدِّث"],
    [fa.FaMapMarkedAlt, C.accent1, "ثلاث محطات", "تنتقلون بالترتيب: استكشاف ← تطبيق ← تقييم"],
    [fa.FaStar, C.accent4, "جمع النقاط", "كل إجابة صحيحة = نجوم، وكل محطة تفتح شارة جديدة"],
    [fa.FaClock, C.accent5, "الوقت محدود", "لكل تحدٍّ وقت محدد يظهر على الشريحة، فالتزموا به"],
  ];
  for (let i = 0; i < 4; i++) {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 6.85 - col * 6.25, y = 1.65 + row * 2.6;
    card(s, x, y, 5.85, 2.2, C.background2, { shadow: undefined });
    await badge(s, x + 4.55, y + 0.45, 1.1, rules[i][1], rules[i][0]);
    txt(s, rules[i][2], { x: x + 0.3, y: y + 0.35, w: 4.1, h: 0.6, fontSize: 22, bold: true, margin: 0 });
    txt(s, rules[i][3], { x: x + 0.3, y: y + 1.0, w: 4.1, h: 1.0, fontSize: 16, color: C.text2, margin: 0 });
  }
  s.addNotes("وزّع الأدوار داخل كل فريق. اعرض لوحة النقاط على السبورة طوال الحصة.");

  // ================= 3. Mission =================
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "البداية" });
  title(s, "المهمة السرية");
  card(s, 0.6, 1.6, 12.1, 1.5, C.text1);
  await badge(s, 11.2, 1.8, 1.1, C.accent4, fa.FaQuestion, H.dk1);
  txt(s, "لماذا تتحرك الكرة عندما نركلها؟ ولماذا تسقط التفاحة إلى الأسفل؟ ولماذا يتوقف الدولاب وحده؟", { x: 0.9, y: 1.6, w: 10.1, h: 1.5, fontSize: 22, bold: true, color: C.background1, valign: "middle" });
  txt(s, "في نهاية المغامرة سيكون كل مستكشف قادرًا على أن:", { x: 0.6, y: 3.4, w: 12.1, h: 0.5, fontSize: 20, bold: true, color: C.accent3 });
  const goals = [
    "يعرّف القوة بأنها دفع أو سحب يؤثر في الجسم",
    "يحدد آثار القوة: تغيير السرعة، أو الاتجاه، أو الشكل",
    "يميّز بين قوى التلامس وقوى عن بُعد (المجال)",
    "يقيس القوة بالنيوتن (N) باستخدام الدينامومتر ويحسب محصلة القوى والوزن",
  ];
  for (let i = 0; i < 4; i++) {
    const y = 4.05 + i * 0.7;
    await badge(s, 12.15, y + 0.05, 0.5, C.accent1, fa.FaCheck);
    txt(s, goals[i], { x: 0.6, y, w: 11.4, h: 0.6, fontSize: 18, valign: "middle", margin: 0 });
  }

  // ================= Station 1 =================
  pres.addSection({ title: "المحطة 1: استكشاف" });
  s = pres.addSlide({ masterName: "SECTION", sectionTitle: "المحطة 1: استكشاف" });
  await badge(s, 5.82, 1.3, 1.7, C.accent1, fa.FaSearch);
  title(s, "المحطة 1: الاستكشاف");
  s.addText("جرّبوا، لاحظوا، سجّلوا… ثم اكتشفوا القاعدة بأنفسكم", { placeholder: "body", ...AR });

  // Explore 1: push & pull
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 1: استكشاف" });
  await chip(s, "استكشاف 1", C.accent1, H.accent1, fa.FaSearch);
  title(s, "تحدّي: حرّك دون أن تلمس؟");
  txt(s, "الأدوات: كرة، سيارة لعبة، خيط، مغناطيس، مشبك ورق، بالون", { x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2 });
  const tasks = [
    [fa.FaHandPaper, "1. حرّك السيارة إلى الأمام ثم أعدها إليك", "ماذا فعلت يدك في كل مرة؟"],
    [fa.FaMagnet, "2. حرّك مشبك الورق دون أن تلمسه", "ما الذي حرّكه؟"],
    [fa.FaWind, "3. افرك البالون بشعرك وقرّبه من قصاصات ورق", "ماذا حدث للقصاصات؟"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 8.75 - i * 4.07;
    card(s, x, 2.05, 3.85, 3.5, C.background2, { shadow: undefined });
    await badge(s, x + 1.37, 2.3, 1.1, C.accent1, tasks[i][0]);
    txt(s, tasks[i][1], { x: x + 0.25, y: 3.55, w: 3.35, h: 1.0, fontSize: 17, bold: true, align: "center" });
    txt(s, tasks[i][2], { x: x + 0.25, y: 4.6, w: 3.35, h: 0.7, fontSize: 16, color: C.accent2, bold: true, align: "center" });
  }
  card(s, 0.6, 5.85, 12.1, 0.9, C.accent4, { shadow: undefined });
  txt(s, "سؤال الاكتشاف: هل يجب أن نلمس الجسم دائمًا لكي نحرّكه؟   ⏱ 7 دقائق   ⭐ نجمتان", { x: 0.8, y: 5.85, w: 11.7, h: 0.9, fontSize: 18, bold: true, valign: "middle" });
  s.addNotes("الهدف: أن يكتشف الطلاب أن القوة دفع أو سحب، وأن بعض القوى تؤثر بالتلامس وبعضها عن بُعد (مغناطيسية، كهربائية ساكنة). لا تعطِ المصطلحات قبل أن يصفوا ملاحظاتهم.");

  // Explore 2: effects of force
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 1: استكشاف" });
  await chip(s, "استكشاف 2", C.accent1, H.accent1, fa.FaSearch);
  title(s, "ماذا تفعل القوة بالأجسام؟");
  txt(s, "نفّذوا كل تجربة واكتبوا ماذا تغيّر في الجسم", { x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2 });
  const rows = [
    ["التجربة", "ماذا تغيّر؟"],
    ["ادفع كرة ساكنة على الطاولة", ""],
    ["أوقف كرة متدحرجة بيدك", ""],
    ["اضرب كرة متحركة جانبيًا بمسطرة", ""],
    ["اضغط على قطعة صلصال", ""],
  ];
  const tRows = rows.map((r, i) => r.map((c) => ({
    text: c,
    options: { ...AR, align: "right", valign: "middle", fontSize: 17, bold: i === 0, color: i === 0 ? C.background1 : C.text1, fill: { color: i === 0 ? C.accent1 : (i % 2 ? C.background2 : C.background1) } },
  })));
  s.addTable(tRows, { x: 4.6, y: 2.0, w: 8.1, colW: [4.6, 3.5], rowH: 0.75, border: { type: "solid", pt: 1, color: "C9D3E3" }, objectName: name("table") });
  // hidden answer key card (teacher reveal)
  card(s, 0.6, 2.0, 3.7, 3.75, C.text1);
  txt(s, "مفتاح الاكتشاف", { x: 0.8, y: 2.15, w: 3.3, h: 0.5, fontSize: 18, bold: true, color: C.accent4 });
  txt(s, [
    { text: "تبدأ الحركة", options: { bullet: true, breakLine: true } },
    { text: "تتوقف الحركة", options: { bullet: true, breakLine: true } },
    { text: "يتغيّر الاتجاه", options: { bullet: true, breakLine: true } },
    { text: "يتغيّر الشكل", options: { bullet: true } },
  ], { x: 0.8, y: 2.7, w: 3.3, h: 2.9, fontSize: 18, color: C.background1, paraSpaceAfter: 10 });
  txt(s, "⏱ 8 دقائق   ⭐ 3 نجوم للفريق الذي يكمل الجدول بدقة", { x: 0.6, y: 6.05, w: 12.1, h: 0.6, fontSize: 16, bold: true, color: C.accent2 });
  s.addNotes("اعرض بطاقة المفتاح بعد أن تنتهي الفرق (يمكن إخفاؤها بإضافة حركة ظهور). الاستنتاج: القوة قد تغيّر سرعة الجسم أو اتجاه حركته أو شكله.");

  // Explore 3: measuring
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 1: استكشاف" });
  await chip(s, "استكشاف 3", C.accent1, H.accent1, fa.FaSearch);
  title(s, "كم تبلغ قوة السحب؟");
  card(s, 8.3, 1.55, 4.4, 4.9, C.background2, { shadow: undefined });
  await badge(s, 9.85, 1.8, 1.3, C.accent1, fa.FaBalanceScale);
  txt(s, "الدينامومتر", { x: 8.5, y: 3.2, w: 4.0, h: 0.6, fontSize: 22, bold: true, align: "center" });
  txt(s, "ميزان نابضي يقيس القوة. كلما زادت القوة استطال النابض أكثر.", { x: 8.55, y: 3.85, w: 3.9, h: 1.3, fontSize: 16, color: C.text2, align: "center" });
  txt(s, "وحدة القوة: النيوتن (N)", { x: 8.5, y: 5.3, w: 4.0, h: 0.7, fontSize: 20, bold: true, color: C.accent1, align: "center" });
  const mrows = [["الجسم المعلَّق أو المسحوب", "التوقع (N)", "القياس (N)"], ["مقلمة", "", ""], ["كتاب العلوم", "", ""], ["حقيبة صغيرة", "", ""], ["سحب درج الطاولة", "", ""]];
  s.addTable(mrows.map((r, i) => r.map((c) => ({ text: c, options: { ...AR, align: "right", valign: "middle", fontSize: 17, bold: i === 0, color: i === 0 ? C.background1 : C.text1, fill: { color: i === 0 ? C.accent1 : (i % 2 ? C.background2 : C.background1) } } }))),
    { x: 0.6, y: 1.55, w: 7.4, colW: [3.6, 1.9, 1.9], rowH: 0.75, border: { type: "solid", pt: 1, color: "C9D3E3" }, objectName: name("table") });
  card(s, 0.6, 5.55, 7.4, 0.9, C.accent4, { shadow: undefined });
  txt(s, "توقّعوا أولًا ثم قيسوا! الفريق الأقرب في توقعاته يربح ⭐⭐", { x: 0.8, y: 5.55, w: 7.0, h: 0.9, fontSize: 17, bold: true, valign: "middle" });
  s.addNotes("درّب الطلاب على قراءة التدريج وضبط المؤشر على الصفر. ناقش: لماذا اختلفت القراءات؟ (أخطاء القراءة، اختلاف الكتلة).");

  // Discovery summary
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 1: استكشاف" });
  await chip(s, "ماذا اكتشفنا؟", C.accent1, H.accent1, fa.FaLightbulb);
  title(s, "ماذا اكتشفنا؟");
  card(s, 0.6, 1.55, 12.1, 1.2, C.text1);
  txt(s, [
    { text: "القوة: ", options: { bold: true, color: C.accent4 } },
    { text: "دفع أو سحب يؤثر في الجسم، وتُقاس بوحدة النيوتن" },
  ], { x: 0.9, y: 1.55, w: 11.5, h: 1.2, fontSize: 24, color: C.background1, valign: "middle" });
  // Force arrow anatomy
  card(s, 6.85, 3.05, 5.85, 3.6, C.background2, { shadow: undefined });
  txt(s, "للقوة ثلاثة عناصر", { x: 7.1, y: 3.15, w: 5.4, h: 0.55, fontSize: 20, bold: true, color: C.accent1 });
  s.addShape(pres.shapes.RECTANGLE, { x: 8.1, y: 4.1, w: 0.9, h: 0.9, fill: { color: C.accent6 }, line: { color: C.accent6 }, objectName: name("box") });
  s.addShape(pres.shapes.LINE, { x: 9.0, y: 4.55, w: 2.6, h: 0, line: { color: C.accent5, width: 5, endArrowType: "triangle" }, objectName: name("arrow") });
  txt(s, "الجسم", { x: 7.8, y: 5.05, w: 1.5, h: 0.4, fontSize: 14, align: "center", color: C.text2 });
  txt(s, "5 N", { rtlMode: false, x: 9.6, y: 3.95, w: 1.4, h: 0.45, fontSize: 18, bold: true, color: C.accent5, align: "center" });
  txt(s, [
    { text: "الشدة: مقدار القوة (5 نيوتن)", options: { bullet: true, breakLine: true } },
    { text: "الاتجاه: إلى أين تؤثر", options: { bullet: true, breakLine: true } },
    { text: "نقطة التأثير: أين تؤثر على الجسم", options: { bullet: true } },
  ], { x: 7.1, y: 5.4, w: 5.4, h: 1.2, fontSize: 15, paraSpaceAfter: 2 });
  // contact vs field
  const kinds = [
    [C.accent2, fa.FaHandRock, "قوى تلامس", "الدفع، السحب، الاحتكاك، رد فعل السطح"],
    [C.accent3, fa.FaMagnet, "قوى عن بُعد", "الجاذبية (الوزن)، المغناطيسية، الكهربائية"],
  ];
  for (let i = 0; i < 2; i++) {
    const y = 3.05 + i * 1.85;
    card(s, 0.6, y, 6.0, 1.65, C.background2, { shadow: undefined });
    await badge(s, 5.25, y + 0.3, 1.05, kinds[i][0], kinds[i][1]);
    txt(s, kinds[i][2], { x: 0.85, y: y + 0.2, w: 4.2, h: 0.55, fontSize: 20, bold: true, margin: 0 });
    txt(s, kinds[i][3], { x: 0.85, y: y + 0.8, w: 4.2, h: 0.7, fontSize: 16, color: C.text2, margin: 0 });
  }
  s.addNotes("هذه الشريحة هي لحظة بناء المفهوم: يقرأ متحدث كل فريق استنتاج فريقه، ثم يقارن المعلم مع هذه الخلاصة. 🏅 تفتح الفرق شارة المستكشف.");

  // ================= Station 2 =================
  pres.addSection({ title: "المحطة 2: تطبيق" });
  s = pres.addSlide({ masterName: "SECTION", sectionTitle: "المحطة 2: تطبيق" });
  await badge(s, 5.82, 1.3, 1.7, C.accent2, fa.FaTools);
  title(s, "المحطة 2: التطبيق");
  s.addText("استخدموا ما اكتشفتموه لحل تحديات جديدة", { placeholder: "body", ...AR });

  // Apply 1: classify
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 2: تطبيق" });
  await chip(s, "تطبيق 1", C.accent2, H.accent2, fa.FaTools);
  title(s, "تحدّي التصنيف السريع");
  txt(s, "صنّفوا كل موقف: قوة تلامس أم قوة عن بُعد؟ ارفعوا البطاقة الصحيحة!", { x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2 });
  const sits = [
    [fa.FaFutbol, "لاعب يركل الكرة"], [fa.FaAppleAlt, "تفاحة تسقط من الشجرة"], [fa.FaMagnet, "مغناطيس يجذب مسمارًا"],
    [fa.FaBicycle, "فرامل الدراجة توقفها"], [fa.FaDoorOpen, "شدّ مقبض الباب"], [fa.FaBolt, "مشط مدلوك يجذب الشعر"],
  ];
  for (let i = 0; i < 6; i++) {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 8.75 - col * 4.07, y = 2.05 + row * 1.85;
    card(s, x, y, 3.85, 1.6, C.background2, { shadow: undefined });
    await badge(s, x + 2.75, y + 0.3, 0.95, C.accent2, sits[i][0]);
    txt(s, sits[i][1], { x: x + 0.2, y: y + 0.2, w: 2.45, h: 1.2, fontSize: 17, bold: true, valign: "middle", margin: 0 });
  }
  card(s, 0.6, 5.85, 12.1, 0.9, C.accent4, { shadow: undefined });
  txt(s, "⏱ 30 ثانية لكل موقف   ⭐ نجمة لكل إجابة صحيحة   الإجابات: تلامس: 1، 4، 5 — عن بُعد: 2، 3، 6", { x: 0.8, y: 5.85, w: 11.7, h: 0.9, fontSize: 16, bold: true, valign: "middle" });
  s.addNotes("وزّع على كل فريق بطاقتين: (تلامس) و(عن بُعد). اقرأ الموقف وعدّ تنازليًا. الترتيب من اليمين: 1 الكرة، 2 التفاحة، 3 المغناطيس، 4 الفرامل، 5 الباب، 6 المشط. يمكن إخفاء سطر الإجابات بحركة ظهور.");

  // Apply 2: tug of war - resultant
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 2: تطبيق" });
  await chip(s, "تطبيق 2", C.accent2, H.accent2, fa.FaTools);
  title(s, "شدّ الحبل: من سيفوز؟");
  card(s, 0.6, 1.5, 12.1, 1.05, C.text1);
  txt(s, [
    { text: "القاعدة: ", options: { bold: true, color: C.accent4 } },
    { text: "نفس الاتجاه ← نجمع القوى   |   اتجاهان متعاكسان ← نطرح، والجسم يتحرك باتجاه القوة الأكبر" },
  ], { x: 0.85, y: 1.5, w: 11.6, h: 1.05, fontSize: 18, color: C.background1, valign: "middle" });
  const tug = [
    ["أ", 60, 40], ["ب", 50, 50], ["ج", 30, 70],
  ];
  for (let i = 0; i < 3; i++) {
    const y = 2.85 + i * 1.15;
    card(s, 0.6, y, 12.1, 0.95, C.background2, { shadow: undefined });
    txt(s, tug[i][0], { x: 11.9, y, w: 0.6, h: 0.95, fontSize: 24, bold: true, color: C.accent2, align: "center", valign: "middle", margin: 0 });
    // right team pulls right, left team pulls left
    s.addShape(pres.shapes.LINE, { x: 8.6, y: y + 0.47, w: 2.9, h: 0, line: { color: C.accent6, width: 5, endArrowType: "triangle" }, objectName: name("arrow") });
    txt(s, `${tug[i][1]} N`, { rtlMode: false, x: 9.3, y: y + 0.02, w: 1.6, h: 0.4, fontSize: 16, bold: true, color: C.accent6, align: "center", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 7.9, y: y + 0.17, w: 0.7, h: 0.6, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: name("box") });
    s.addShape(pres.shapes.LINE, { x: 5.0, y: y + 0.47, w: 2.9, h: 0, flipH: true, line: { color: C.accent5, width: 5, endArrowType: "triangle" }, objectName: name("arrow") });
    txt(s, `${tug[i][2]} N`, { rtlMode: false, x: 5.6, y: y + 0.02, w: 1.6, h: 0.4, fontSize: 16, bold: true, color: C.accent5, align: "center", margin: 0 });
    txt(s, "المحصلة = ____ نيوتن   الاتجاه: ______", { x: 0.8, y, w: 4.0, h: 0.95, fontSize: 16, valign: "middle", margin: 0 });
  }
  txt(s, "⏱ 5 دقائق   ⭐ نجمتان لكل حالة صحيحة (المقدار + الاتجاه)", { x: 0.6, y: 6.35, w: 12.1, h: 0.5, fontSize: 16, bold: true, color: C.accent2 });
  s.addNotes("الإجابات: أ) 20 N نحو اليمين (الأزرق). ب) 0 N — القوى متوازنة ولا يتحرك الجسم. ج) 40 N نحو اليسار (الأحمر). نشاط حركي اختياري: شدّ حبل حقيقي بين فريقين مع دينامومترين.");

  // Apply 3: weight
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 2: تطبيق" });
  await chip(s, "تطبيق 3", C.accent2, H.accent2, fa.FaTools);
  title(s, "رحلة إلى القمر: كم وزنك؟");
  card(s, 7.3, 1.55, 5.4, 2.4, C.text1);
  txt(s, "الوزن = الكتلة × شدة الجاذبية", { x: 7.5, y: 1.7, w: 5.0, h: 0.7, fontSize: 22, bold: true, color: C.accent4, align: "center" });
  txt(s, "W = m × g", { x: 7.5, y: 2.4, w: 5.0, h: 0.7, fontSize: 30, bold: true, color: C.background1, align: "center", rtlMode: false });
  txt(s, "الأرض: 10 نيوتن/كغ   ·   القمر: 1.6 نيوتن/كغ", { x: 7.5, y: 3.15, w: 5.0, h: 0.6, fontSize: 15, color: C.background2, align: "center" });
  card(s, 7.3, 4.2, 5.4, 2.45, C.background2, { shadow: undefined });
  await badge(s, 11.5, 4.45, 0.95, C.accent3, fa.FaMoon);
  txt(s, "تذكّر: الكتلة لا تتغيّر من مكان لآخر، أمّا الوزن فيتغيّر لأنه قوة جذب.", { x: 7.5, y: 4.4, w: 3.9, h: 2.1, fontSize: 17, valign: "middle" });
  const wrows = [["رائد الفضاء", "الكتلة", "الوزن على الأرض", "الوزن على القمر"], ["سامي", "40 كغ", "", ""], ["ليلى", "50 كغ", "", ""], ["حقيبة المعدات", "20 كغ", "", ""]];
  s.addTable(wrows.map((r, i) => r.map((c) => ({ text: c, options: { ...AR, align: "center", valign: "middle", fontSize: 16, bold: i === 0, color: i === 0 ? C.background1 : C.text1, fill: { color: i === 0 ? C.accent2 : (i % 2 ? C.background2 : C.background1) } } }))),
    { x: 0.6, y: 1.55, w: 6.4, colW: [1.8, 1.2, 1.7, 1.7], rowH: [0.9, 0.8, 0.8, 0.8], border: { type: "solid", pt: 1, color: "C9D3E3" }, objectName: name("table") });
  card(s, 0.6, 5.35, 6.4, 1.3, C.accent4, { shadow: undefined });
  txt(s, "سؤال المكافأة ⭐⭐⭐: لماذا يقفز رائد الفضاء على القمر أعلى بكثير مما يقفز على الأرض؟", { x: 0.8, y: 5.35, w: 6.0, h: 1.3, fontSize: 16, bold: true, valign: "middle" });
  s.addNotes("الإجابات: سامي 400 N / 64 N. ليلى 500 N / 80 N. الحقيبة 200 N / 32 N. المكافأة: لأن قوة الجاذبية على القمر أصغر (نحو سدس جاذبية الأرض)، فيكون وزنه أقل. 🏅 تفتح الفرق شارة المهندس.");

  // ================= Station 3 =================
  pres.addSection({ title: "المحطة 3: تقييم" });
  s = pres.addSlide({ masterName: "SECTION", sectionTitle: "المحطة 3: تقييم" });
  await badge(s, 5.82, 1.3, 1.7, C.accent3, fa.FaTrophy);
  title(s, "المحطة 3: التقييم");
  s.addText("التحدي النهائي: من سيكون بطل القوى؟", { placeholder: "body", ...AR });

  // Quiz slides
  const quiz = [
    ["الوحدة المستخدمة لقياس القوة هي:", ["الكيلوغرام", "النيوتن", "المتر", "الثانية"], 1],
    ["أيٌّ مما يلي قوة عن بُعد؟", ["الاحتكاك", "دفع عربة", "الجاذبية", "شدّ حبل"], 2],
    ["عندما تضرب الكرة المتحركة بالمضرب فإن القوة تغيّر:", ["لونها", "كتلتها", "اتجاه حركتها", "مادتها"], 2],
    ["قوتان كلٌّ منهما 30 نيوتن في اتجاهين متعاكسين، محصلتهما:", ["60 نيوتن", "30 نيوتن", "15 نيوتن", "0 نيوتن"], 3],
    ["جسم كتلته 8 كغ على الأرض، وشدة الجاذبية 10 نيوتن/كغ. وزنه:", ["80 نيوتن", "8 نيوتن", "18 نيوتن", "0.8 نيوتن"], 0],
  ];
  const letters = ["أ", "ب", "ج", "د"];
  const optCols = [C.accent1, C.accent2, C.accent3, C.accent6];
  for (let q = 0; q < quiz.length; q++) {
    s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 3: تقييم" });
    await chip(s, `سؤال ${q + 1} من 5`, C.accent3, H.accent3, fa.FaTrophy);
    title(s, "التحدي النهائي");
    card(s, 0.6, 1.55, 12.1, 1.5, C.text1);
    txt(s, quiz[q][0], { x: 0.9, y: 1.55, w: 11.5, h: 1.5, fontSize: 28, bold: true, color: C.background1, valign: "middle" });
    for (let o = 0; o < 4; o++) {
      const col = o % 2, row = Math.floor(o / 2);
      const x = 6.85 - col * 6.25, y = 3.35 + row * 1.55;
      card(s, x, y, 5.85, 1.3, optCols[o]);
      s.addShape(pres.shapes.OVAL, { x: x + 4.65, y: y + 0.2, w: 0.9, h: 0.9, fill: { color: C.background1 }, line: { color: C.background1 }, objectName: name("letter") });
      txt(s, letters[o], { x: x + 4.65, y: y + 0.2, w: 0.9, h: 0.9, fontSize: 24, bold: true, color: optCols[o], align: "center", valign: "middle", margin: 0 });
      txt(s, quiz[q][1][o], { x: x + 0.3, y, w: 4.2, h: 1.3, fontSize: 24, bold: true, color: C.background1, valign: "middle", margin: 0 });
    }
    txt(s, "⏱ 20 ثانية   ⭐ نجمتان للإجابة الصحيحة", { x: 0.6, y: 6.5, w: 12.1, h: 0.45, fontSize: 15, bold: true, color: C.accent3 });
    s.addNotes(`الإجابة الصحيحة: (${letters[quiz[q][2]]}) ${quiz[q][1][quiz[q][2]]}. تكتب الفرق الحرف على لوح صغير وترفعه معًا عند انتهاء الوقت.`);
  }

  // Answer key
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 3: تقييم" });
  await chip(s, "الإجابات", C.accent3, H.accent3, fa.FaCheck);
  title(s, "مفتاح الإجابات");
  const why = [
    "النيوتن (N) هو وحدة قياس القوة",
    "الجاذبية تؤثر دون تلامس",
    "القوة تغيّر اتجاه حركة الجسم",
    "قوتان متساويتان ومتعاكستان ← متوازنتان",
    "W = 8 × 10 = 80 N",
  ];
  for (let q = 0; q < 5; q++) {
    const y = 1.55 + q * 1.0;
    card(s, 0.6, y, 12.1, 0.82, q % 2 ? C.background1 : C.background2, { shadow: undefined });
    s.addShape(pres.shapes.OVAL, { x: 11.85, y: y + 0.11, w: 0.6, h: 0.6, fill: { color: C.accent3 }, line: { color: C.accent3 }, objectName: name("num") });
    txt(s, String(q + 1), { x: 11.85, y: y + 0.11, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
    const a = quiz[q][2];
    txt(s, `(${letters[a]}) ${quiz[q][1][a]}`, { x: 8.0, y, w: 3.65, h: 0.82, fontSize: 20, bold: true, color: optCols[a], valign: "middle", margin: 0 });
    txt(s, why[q], { rtlMode: q !== 4, x: 0.85, y, w: 7.0, h: 0.82, fontSize: 17, color: C.text2, valign: "middle", margin: 0 });
  }

  // Exit ticket
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 3: تقييم" });
  await chip(s, "بطاقة خروج", C.accent3, H.accent3, fa.FaPen);
  title(s, "بطاقة الخروج الفردية");
  txt(s, "يجيب كل مستكشف وحده على ورقة صغيرة قبل مغادرة الصف", { x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2 });
  const exit = [
    [C.accent1, "3", "أشياء تعلمتها اليوم عن القوى"],
    [C.accent2, "2", "مثالان من حياتي اليومية على قوة تلامس وقوة عن بُعد"],
    [C.accent3, "1", "سؤال ما زلت أفكّر فيه"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 8.75 - i * 4.07;
    card(s, x, 2.1, 3.85, 3.6, C.background2, { shadow: undefined });
    s.addShape(pres.shapes.OVAL, { x: x + 1.27, y: 2.35, w: 1.3, h: 1.3, fill: { color: exit[i][0] }, line: { color: exit[i][0] }, objectName: name("num") });
    txt(s, exit[i][1], { x: x + 1.27, y: 2.35, w: 1.3, h: 1.3, fontSize: 44, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
    txt(s, exit[i][2], { x: x + 0.25, y: 3.9, w: 3.35, h: 1.6, fontSize: 19, bold: true, align: "center", valign: "top" });
  }
  card(s, 0.6, 6.0, 12.1, 0.8, C.text1, { shadow: undefined });
  txt(s, "تقييم ذاتي: ضع إشارة على مستواك →   😀 أستطيع شرحه لزميلي   🙂 فهمته   😐 أحتاج مساعدة", { x: 0.8, y: 6.0, w: 11.7, h: 0.8, fontSize: 17, bold: true, color: C.background1, valign: "middle" });

  // Rubric
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "المحطة 3: تقييم" });
  await chip(s, "سلّم التقدير", C.accent3, H.accent3, fa.FaClipboardCheck);
  title(s, "سلّم تقدير أداء الفرق");
  const rub = [
    ["المعيار", "ممتاز ⭐⭐⭐", "جيد ⭐⭐", "يحتاج دعمًا ⭐"],
    ["الاستكشاف", "ملاحظات دقيقة وتوقعات مبرَّرة", "ملاحظات صحيحة ناقصة", "ملاحظات قليلة غير دقيقة"],
    ["التطبيق", "حسابات صحيحة مع الوحدة والاتجاه", "حسابات صحيحة دون وحدة أو اتجاه", "أخطاء في الحساب"],
    ["التقييم", "4–5 إجابات صحيحة", "3 إجابات صحيحة", "أقل من 3"],
    ["العمل الجماعي", "كل الأدوار فاعلة والتزام بالوقت", "معظم الأدوار فاعلة", "مشاركة فرد أو اثنين"],
  ];
  const rubFill = [C.text1, C.accent1, C.accent2, C.accent5];
  s.addTable(rub.map((r, i) => r.map((c, j) => ({ text: c, options: { ...AR, align: j === 0 ? "right" : "center", valign: "middle", fontSize: 16, bold: i === 0 || j === 0, color: i === 0 ? C.background1 : C.text1, fill: { color: i === 0 ? rubFill[j] : (j === 0 ? C.background2 : C.background1) } } }))),
    { x: 0.6, y: 1.55, w: 12.1, colW: [2.5, 3.2, 3.2, 3.2], rowH: [0.8, 1.0, 1.0, 1.0, 1.0], border: { type: "solid", pt: 1, color: "C9D3E3" }, objectName: name("table") });
  txt(s, "مجموع النجوم يحدد الشارة النهائية للفريق", { x: 0.6, y: 6.5, w: 12.1, h: 0.45, fontSize: 16, bold: true, color: C.accent3 });

  // ================= Finale =================
  pres.addSection({ title: "الختام" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "الختام" });
  s.background = { color: H.dk1 };
  s.addText("لوحة الأبطال", { placeholder: "title", ...AR, color: C.background1 });
  const medals = [
    [C.accent4, fa.FaCrown, "بطل القوى", "أكثر من 30 نجمة"],
    ["C0C7D1", fa.FaMedal, "مهندس القوى", "20 – 30 نجمة"],
    ["CD8B4E", fa.FaAward, "مستكشف القوى", "أقل من 20 نجمة"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 8.75 - i * 4.07;
    card(s, x, 1.7, 3.85, 3.6, C.text2, { shadow: undefined });
    await badge(s, x + 1.17, 1.95, 1.5, medals[i][0], medals[i][1], H.dk1);
    txt(s, medals[i][2], { x: x + 0.2, y: 3.6, w: 3.45, h: 0.7, fontSize: 24, bold: true, color: C.background1, align: "center" });
    txt(s, medals[i][3], { x: x + 0.2, y: 4.35, w: 3.45, h: 0.6, fontSize: 18, color: C.accent4, align: "center" });
  }
  txt(s, "القوة في كل مكان حولنا… والآن أصبحتم تعرفون كيف تكتشفونها وتقيسونها!", { x: 0.6, y: 5.7, w: 12.1, h: 0.9, fontSize: 22, bold: true, color: C.background1, align: "center", valign: "middle" });
  s.addNotes("احسب النجوم على لوحة النقاط وأعلن الشارات. ثمن جهد كل الفرق.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
